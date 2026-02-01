# OpenCode Telegram Bridge

[![English Docs](https://img.shields.io/badge/English_Docs-README.md-red)](README.md)

通过 Telegram 使用本地 OpenCode。

> 🌐 **双语支持** • [English](README.md) • [中文](README_CN.md)
>
> 👆 **English users**: [Click here for English documentation](README.md)

## 功能

这个桥接工具让你通过 Telegram 使用本地 OpenCode。在手机上发送消息，接收 OpenCode 的 AI 回复。

**工作流程：**
1. 在 Telegram 发送消息
2. 桥接工具转发到本地 OpenCode（4096端口）
3. OpenCode 使用 Sisyphus agent 处理
4. 在 Telegram 收到回复

## 特性

- 💬 **双向通信** - 发送到 OpenCode，在 Telegram 接收回复
- 🔄 **持久会话** - 每个用户拥有独立的 OpenCode 会话
- 🆕 **会话重置** - `/reset` 命令开启新对话
- 🛡️ **错误处理** - 记录日志并处理连接问题
- ⚙️ **模型选择** - 可配置模型（默认：opencode/glm-4.7-free）
- 🌍 **双语文档** - 中英文文档

## 快速开始

### 要求
- Python 3.10+
- 本地运行 OpenCode（4096端口）
- Telegram Bot Token（从 @BotFather 获取）

### 安装

```bash
pip install -r requirements.txt

cp .env.example .env
# 编辑 .env 添加你的 BOT_TOKEN

python3 bot.py
```

### 配置 (.env)

```env
BOT_TOKEN=your_telegram_bot_token_here
OPENCODE_URL=http://localhost:4096
DEFAULT_MODEL=opencode/glm-4.7-free
```

## 使用

### 命令
- `/start` - 欢迎信息
- `/help` - 显示帮助
- `/reset` - 重置 OpenCode 会话

### 发送消息
直接发送文本消息即可。桥接工具会：
1. 转发到 OpenCode
2. 等待响应
3. 在 Telegram 回复你

## 架构

```
Telegram App → Python Bridge → OpenCode API → AI Model
     ↑              ↓               ↓
   Response ←  httpx client    Sisyphus agent
```

## 文件

- `bot.py` - 主程序（polling 模式）
- `bot_webhook.py` - Webhook 模式
- `requirements.txt` - Python 依赖
- `.env.example` - 配置模板

## 故障排除

**Bot 无响应：**
- 检查 OpenCode 运行状态：`lsof -i :4096`
- 查看日志：`tail -f logs/bot.log`
- 验证 token：`python3 verify_token.py`

**连接错误：**
- 确认 OpenCode 可访问：`curl http://localhost:4096/session`
- 检查 `.env` 中的 `OPENCODE_URL`

## 安全

- 不要提交 `.env` 文件（包含 token）
- 保管好 bot token
- 使用 polling 模式（简单，适合开发）

## 许可证

MIT
