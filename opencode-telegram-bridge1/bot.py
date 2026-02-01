import os
import asyncio
import logging
from typing import Dict, Optional

import httpx
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.request import HTTPXRequest

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENCODE_URL = os.getenv("OPENCODE_URL", "http://localhost:4096")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "opencode/glm-4.7-free")


def parse_model(model_str: str):
    """Parse model string (e.g., 'opencode/glm-4.7-free') into model object"""
    parts = model_str.split("/")
    if len(parts) == 2:
        return {"providerID": parts[0], "modelID": parts[1]}
    return {"providerID": "opencode", "modelID": "glm-4.7-free"}


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

# OpenCode HTTP client
opencode_client = httpx.AsyncClient(
    base_url=OPENCODE_URL,
    timeout=300.0,  # 5 minutes timeout for long-running tasks
)

# Store user sessions: {user_id: session_id}
user_sessions: Dict[int, str] = {}


async def create_opencode_session() -> str:
    """Create a new OpenCode session and return session_id"""
    try:
        response = await opencode_client.post(
            "/session", json={"title": "Telegram Session"}
        )
        response.raise_for_status()
        data = response.json()
        return data["id"]
    except Exception as e:
        logger.error(f"Failed to create OpenCode session: {e}")
        raise


async def get_or_create_session(user_id: int) -> str:
    """Get existing session for user or create a new one"""
    if user_id not in user_sessions:
        logger.info(f"Creating new session for user {user_id}")
        session_id = await create_opencode_session()
        user_sessions[user_id] = session_id
    return user_sessions[user_id]


async def send_to_opencode(session_id: str, message: str) -> str:
    """Send message to OpenCode and return response"""
    try:
        model_obj = parse_model(DEFAULT_MODEL)
        response = await opencode_client.post(
            f"/session/{session_id}/message",
            json={
                "model": model_obj,
                "agent": "sisyphus",
                "parts": [{"type": "text", "text": message}],
            },
        )
        response.raise_for_status()
        data = response.json()

        # Check for errors first
        if "error" in data and data["error"]:
            error_data = data.get("error", {})
            error_msg = error_data.get("data", {}).get("message", str(error_data))
            logger.error(f"OpenCode API error: {error_msg}")
            return f"❌ OpenCode Error: {error_msg[:500]}"

        # Extract the assistant's response from parts
        # Check for parts in response
        parts = data.get("parts", [])

        # Handle both list and dict response formats
        if isinstance(parts, list):
            for part in parts:
                if isinstance(part, dict) and part.get("type") == "text":
                    return part.get("text", "")

        return "Message sent to OpenCode (waiting for response...)"

    except Exception as e:
        logger.error(f"Failed to send message to OpenCode: {e}")
        return f"Error communicating with OpenCode: {str(e)}"


async def handle_update(update):
    """Handle Telegram update"""
    # Import here to avoid issues with telegram package
    from telegram import Update

    # Convert dict to Update object if needed
    if isinstance(update, dict):
        update = Update.de_json(update, Bot(token=BOT_TOKEN, request=HTTPXRequest()))

    # Get message
    message = update.message
    if not message or not message.text:
        return

    # Extract user info
    user = message.from_user
    user_message = message.text
    user_id = user.id
    chat_id = message.chat_id

    logger.info(
        f"Received message from {user.username or user.first_name} (ID={user_id}): {user_message}"
    )

    bot = Bot(token=BOT_TOKEN, request=HTTPXRequest())

    # Handle commands
    if user_message.startswith("/"):
        if user_message == "/start":
            await bot.send_message(
                chat_id=chat_id,
                text=f"👋 Hello, {user.first_name}!\n\n"
                "I'm your OpenCode assistant.\n"
                "Send me any message and I'll forward it to OpenCode for processing.\n\n"
                "Commands:\n"
                "/start - Show this welcome message\n"
                "/help - Show help information\n"
                "/reset - Create a new session",
            )
        elif user_message == "/help":
            await bot.send_message(
                chat_id=chat_id,
                text="📖 **Help**\n\n"
                "Just send me a message and I'll forward it to OpenCode.\n\n"
                "Available commands:\n"
                "/start - Start the bot\n"
                "/help - Show this help\n"
                "/reset - Reset your session and start fresh",
            )
        elif user_message == "/reset":
            if user_id in user_sessions:
                old_session_id = user_sessions[user_id]
                del user_sessions[user_id]
                logger.info(f"Reset session for user {user_id} (was {old_session_id})")

            await get_or_create_session(user_id)
            await bot.send_message(
                chat_id=chat_id, text="✅ Session reset! Starting fresh."
            )
        return

    # Handle regular messages
    try:
        # Send "typing" action
        await bot.send_chat_action(chat_id=chat_id, action="typing")

        # Get or create session for this user
        session_id = await get_or_create_session(user_id)
        logger.info(f"Using session {session_id} for user {user_id}")

        # Send message to OpenCode
        response = await send_to_opencode(session_id, user_message)

        # Limit response length to avoid Telegram message size limits (4096 chars)
        if len(response) > 4000:
            response = response[:4000] + "\n\n... (response truncated)"

        # Send response back to Telegram
        await bot.send_message(chat_id=chat_id, text=response)
        logger.info(f"Sent response to user {user_id}")

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        await bot.send_message(
            chat_id=chat_id,
            text=f"❌ Sorry, an error occurred while processing your message.\n\n"
            f"Error: {str(e)}",
        )


async def poll_updates():
    """Poll for updates from Telegram"""
    bot = Bot(token=BOT_TOKEN, request=HTTPXRequest())

    logger.info("Starting Telegram bot with polling...")
    offset = 0

    while True:
        try:
            updates = await bot.get_updates(offset=offset, timeout=30)

            if updates:
                for update in updates:
                    await handle_update(update)
                    offset = update.update_id + 1

        except Exception as e:
            logger.error(f"Error polling updates: {e}", exc_info=True)
            await asyncio.sleep(5)


def main():
    """Start bot"""
    try:
        asyncio.run(poll_updates())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        # Close OpenCode client
        asyncio.run(opencode_client.aclose())


if __name__ == "__main__":
    main()
