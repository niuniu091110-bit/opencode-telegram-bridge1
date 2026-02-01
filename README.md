# OpenCode Telegram Bridge

🌐 **English** | **中文**

---

## English Description

Connect your local OpenCode instance to Telegram for remote AI interaction.

### What It Does

This bridge enables you to use OpenCode's AI capabilities directly from Telegram. Send messages from your phone or any device, and receive intelligent responses powered by OpenCode's agent.

### Features

- 💬 **Two-way Messaging** - Send prompts to OpenCode, receive AI responses in Telegram
- 🔄 **Persistent Sessions** - Each user maintains their own OpenCode session context
- 🆕 **Session Reset** - Use `/reset` to start a fresh conversation
- 🛡️ **Error Handling** - Robust logging and connection error management
- ⚙️ **Model Selection** - Configurable AI model (default: opencode/glm-4.7-free)
- 🌍 **Bilingual** - Full documentation in English and Chinese

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your BOT_TOKEN

# Start the bot
python3 bot.py
```

### Requirements

- Python 3.10+
- OpenCode running locally on port 4096
- Telegram Bot Token (get one from @BotFather)

### License

MIT

---

## 中文描述

通过 Telegram 远程使用本地 OpenCode 的 AI 能力。

### 功能介绍

这个桥接工具让你可以直接在 Telegram 中使用 OpenCode 的强大 AI 功能。随时随地发送消息，接收由 OpenCode  agent 生成的智能回复。

### 主要特性

- 💬 **双向通信** - 发送提示词到 OpenCode，在 Telegram 接收 AI 回复
- 🔄 **持久会话** - 每个用户保持独立的 OpenCode 会话上下文
- 🆕 **会话重置** - 使用 `/reset` 开始新对话
- 🛡️ **错误处理** - 完善的日志记录和连接错误管理
- ⚙️ **模型选择** - 可配置 AI 模型（默认：opencode/glm-4.7-free）
- 🌍 **双语文档** - 提供完整的中英文文档

### 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置
cp .env.example .env
# 编辑 .env 添加你的 BOT_TOKEN

# 启动机器人
python3 bot.py
```

### 环境要求

- Python 3.10+
- 本地运行 OpenCode（4096 端口）
- Telegram Bot Token（从 @BotFather 获取）

### 开源协议

MIT
