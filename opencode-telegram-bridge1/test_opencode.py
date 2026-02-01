#!/usr/bin/env python3
"""Test script to verify OpenCode API is working correctly"""

import asyncio
import httpx
import json


async def test_opencode():
    """Test OpenCode API endpoints"""
    base_url = "http://localhost:4096"

    print("🧪 Testing OpenCode API...")
    print("=" * 50)

    async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as client:
        # Test 1: List sessions
        print("\n1️⃣  Testing GET /session...")
        try:
            response = await client.get("/session")
            response.raise_for_status()
            data = response.json()
            print(f"   ✅ Success! Found {len(data)} existing sessions")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            return False

        # Test 2: Create a new session
        print("\n2️⃣  Testing POST /session...")
        try:
            response = await client.post("/session", json={"title": "Test Session"})
            response.raise_for_status()
            data = response.json()
            session_id = data["id"]
            print(f"   ✅ Success! Created session: {session_id}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            return False

        # Test 3: Send a message to the session
        print("\n3️⃣  Testing POST /session/{id}/message...")
        try:
            response = await client.post(
                f"/session/{session_id}/message",
                json={
                    "agent": "sisyphus",
                    "parts": [
                        {
                            "type": "text",
                            "text": "Hello OpenCode! This is a test message.",
                        }
                    ],
                },
            )
            response.raise_for_status()
            data = response.json()

            # Print response
            print(f"   ✅ Success! Received response:")
            print(f"   Message ID: {data.get('info', {}).get('id')}")
            print(f"   Parts count: {len(data.get('parts', []))}")

            # Print first text part
            for part in data.get("parts", []):
                if part.get("type") == "text":
                    text = part.get("text", "")
                    preview = text[:100] + "..." if len(text) > 100 else text
                    print(f"   Response preview: {preview}")
                    break

        except Exception as e:
            print(f"   ❌ Failed: {e}")
            if hasattr(e, "response"):
                print(f"   Response: {e.response.text}")
            return False

        # Test 4: List tools
        print("\n4️⃣  Testing GET /experimental/tool/ids...")
        try:
            response = await client.get("/experimental/tool/ids")
            response.raise_for_status()
            data = response.json()
            tools = data.get("tool_ids", [])
            print(f"   ✅ Success! Found {len(tools)} available tools")
            print(f"   Sample tools: {tools[:5]}...")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            return False

    print("\n" + "=" * 50)
    print("✅ All tests passed! OpenCode API is working correctly.")
    print("\n🚀 You can now start the Telegram bot:")
    print("   python3 bot.py")
    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(test_opencode())
        exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Test interrupted by user")
        exit(1)
