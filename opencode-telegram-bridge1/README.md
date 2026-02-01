# OpenCode Telegram Bridge

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![中文文档](https://img.shields.io/badge/中文文档-README_CN.md-red)](README_CN.md)

Connect your local OpenCode to Telegram for remote interaction.

> 🌐 **Bilingual** • [English](README.md) • [中文](README_CN.md)
>
> 👆 **中文用户**: [点击这里查看中文文档](README_CN.md)

## What It Does

This bridge lets you use your local OpenCode instance through Telegram. Send messages from your phone and get AI responses from OpenCode.

**How it works:**
1. You send a message in Telegram
2. The bridge forwards it to your local OpenCode (port 4096)
3. OpenCode processes with the Sisyphus agent
4. You receive the response back in Telegram

## Features

- 💬 **Two-way messaging** - Send to OpenCode, receive responses in Telegram
- 🔄 **Persistent sessions** - Each user keeps their own OpenCode session
- 🆕 **Session reset** - `/reset` command to start a fresh conversation
- 🛡️ **Error handling** - Logs errors and handles connection issues
- ⚙️ **Model selection** - Configurable model (default: opencode/glm-4.7-free)
- 🌍 **Bilingual** - Documentation in English and Chinese

## Quick Start

### Requirements
- Python 3.10+
- OpenCode running locally on port 4096
- Telegram Bot Token (from @BotFather)

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your BOT_TOKEN

# Start
python3 bot.py
```

### Configuration (.env)

```env
BOT_TOKEN=your_telegram_bot_token_here
OPENCODE_URL=http://localhost:4096
DEFAULT_MODEL=opencode/glm-4.7-free
```

## Usage

### Commands
- `/start` - Welcome message
- `/help` - Show help
- `/reset` - Reset your OpenCode session

### Sending Messages
Just send any text message to your bot. The bridge will:
1. Forward it to OpenCode
2. Wait for the response
3. Send it back to you in Telegram

## Architecture

```
Telegram App → Python Bridge → OpenCode API → AI Model
     ↑              ↓               ↓
   Response ←  httpx client    Sisyphus agent
```

## Files

- `bot.py` - Main bot (polling mode)
- `bot_webhook.py` - Webhook mode alternative
- `requirements.txt` - Python dependencies
- `.env.example` - Configuration template

## Troubleshooting

**Bot doesn't respond:**
- Check OpenCode is running: `lsof -i :4096`
- Check logs: `tail -f logs/bot.log`
- Verify token: `python3 verify_token.py`

**Connection errors:**
- Ensure OpenCode is accessible: `curl http://localhost:4096/session`
- Check `OPENCODE_URL` in `.env`

## Security

- Never commit `.env` file (contains your token)
- Keep your bot token private
- Uses polling mode (simpler, good for development)

## License

MIT
