#!/bin/bash

# OpenCode Telegram Bridge Setup Script

set -e

echo "🚀 Setting up OpenCode Telegram Bridge..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Check if OpenCode is running
echo ""
echo "📋 Checking if OpenCode is running..."
if lsof -i :4096 > /dev/null 2>&1; then
    echo "✅ OpenCode is running on port 4096"
else
    echo "⚠️  OpenCode is not running on port 4096"
    echo "   Starting OpenCode..."
    opencode serve --port=4096 > /tmp/opencode.log 2>&1 &
    sleep 3
    if lsof -i :4096 > /dev/null 2>&1; then
        echo "✅ OpenCode started successfully"
    else
        echo "❌ Failed to start OpenCode. Please start it manually:"
        echo "   opencode serve --port=4096"
        exit 1
    fi
fi

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if .env exists
echo ""
echo "📋 Checking configuration..."
if [ ! -f .env ]; then
    echo "⚠️  .env file not found."
    echo ""
    echo "🤖 Let's create a Telegram Bot and configure it!"
    echo ""
    read -p "Do you want to run the interactive bot setup guide? (y/n): " run_guide
    if [ "$run_guide" = "y" ] || [ "$run_guide" = "Y" ]; then
        echo ""
        echo "🚀 Starting interactive bot setup..."
        python3 create_bot.py
        if [ $? -ne 0 ]; then
            echo ""
            echo "❌ Bot setup failed or was cancelled"
            exit 1
        fi
    else
        echo "Creating .env from template..."
        cp .env.example .env
        echo ""
        echo "❗ IMPORTANT: Edit .env and add your BOT_TOKEN from @BotFather"
        echo "   nano .env"
        echo ""
        read -p "Press Enter after you've added your BOT_TOKEN..."
    fi
else
    echo "✅ .env file exists"
fi

# Test OpenCode connection
echo ""
echo "📋 Testing OpenCode connection..."
if curl -s http://localhost:4096/session > /dev/null 2>&1; then
    echo "✅ OpenCode is accessible"
else
    echo "❌ Cannot connect to OpenCode at http://localhost:4096"
    echo "   Make sure OpenCode is running and accessible"
    exit 1
fi

# Check BOT_TOKEN in .env
echo ""
echo "📋 Checking BOT_TOKEN..."
if grep -q "your_telegram_bot_token_here" .env; then
    echo "⚠️  BOT_TOKEN is not set in .env"
    echo "   Please edit .env and add your actual token from @BotFather"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 Next steps:"
echo "   1. Make sure you've added your BOT_TOKEN to .env"
echo "   2. Start the bot: python3 bot.py"
echo "   3. Open Telegram and find your bot"
echo "   4. Send /start to begin"
echo ""
echo "📚 For more info, see README.md"
