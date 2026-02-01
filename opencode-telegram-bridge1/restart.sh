#!/bin/bash

echo "🧹 Cleaning Telegram Bot connection..."
echo ""

# Load token from environment or .env file
if [ -z "$BOT_TOKEN" ] && [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

if [ -n "$BOT_TOKEN" ]; then
    echo "1. Deleting webhook..."
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/deleteWebhook" > /dev/null
fi

echo "2. Waiting for cleanup..."
sleep 5

echo "3. Cleaning local processes..."
pkill -9 -f "python3.*bot.py" 2>/dev/null
sleep 2

echo "✅ Cleanup complete!"
echo ""
echo "🚀 Starting Bot..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$(dirname "$0")"
python3 bot.py
