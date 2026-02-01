#!/usr/bin/env python3
"""
Production-ready Telegram Bot using Webhook instead of polling
"""

import os
import asyncio
import logging
from typing import Dict, Optional

import httpx
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
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
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
PORT = int(os.getenv("PORT", 8443))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL environment variable is required for webhook mode")

# OpenCode HTTP client
opencode_client = httpx.AsyncClient(base_url=OPENCODE_URL, timeout=300.0)

# Store user sessions: {user_id: session_id}
user_sessions: Dict[int, str] = {}


async def create_opencode_session() -> str:
    """Create a new OpenCode session"""
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
    """Get or create session for user"""
    if user_id not in user_sessions:
        logger.info(f"Creating new session for user {user_id}")
        session_id = await create_opencode_session()
        user_sessions[user_id] = session_id
    return user_sessions[user_id]


async def send_to_opencode(session_id: str, message: str) -> str:
    """Send message to OpenCode"""
    try:
        response = await opencode_client.post(
            f"/session/{session_id}/message",
            json={"agent": "sisyphus", "parts": [{"type": "text", "text": message}]},
        )
        response.raise_for_status()
        data = response.json()

        parts = data.get("parts", [])
        if isinstance(parts, list):
            for part in parts:
                if isinstance(part, dict) and part.get("type") == "text":
                    return part.get("text", "")

        return "Message sent to OpenCode (processing...)"
    except Exception as e:
        logger.error(f"Failed to send to OpenCode: {e}")
        return f"Error: {str(e)}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello, {user.first_name}!\n\n"
        "I'm your OpenCode assistant via Webhook.\n"
        "Send me any message and I'll forward it to OpenCode.\n\n"
        "Commands: /start, /help, /reset"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    await update.message.reply_text(
        "📖 **Help**\n\n"
        "Just send me a message and I'll forward it to OpenCode.\n\n"
        "Available commands:\n"
        "/start - Start bot\n"
        "/help - Show this help\n"
        "/reset - Reset your session"
    )


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /reset command"""
    user_id = update.effective_user.id
    if user_id in user_sessions:
        del user_sessions[user_id]
        logger.info(f"Reset session for user {user_id}")
    await get_or_create_session(user_id)
    await update.message.reply_text("✅ Session reset!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages"""
    if not update.message or not update.message.text:
        return

    user = update.effective_user
    user_message = update.message.text
    user_id = user.id

    logger.info(f"Received from {user.username or user.first_name}: {user_message}")

    try:
        await update.message.chat.send_action(action="typing")

        session_id = await get_or_create_session(user_id)

        response = await send_to_opencode(session_id, user_message)

        if len(response) > 4000:
            response = response[:4000] + "\n\n... (truncated)"

        await update.message.reply_text(response)

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Start bot with webhook"""
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Add error handler
    application.add_error_handler(error_handler)

    logger.info(f"Starting bot with webhook on port {PORT}")
    logger.info(f"Webhook URL: {WEBHOOK_URL}/webhook")

    # Run with webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook",
        secret_token=WEBHOOK_SECRET,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        asyncio.run(opencode_client.aclose())
