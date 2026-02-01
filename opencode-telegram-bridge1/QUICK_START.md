╔═════════════════════════════════════════════════════════════╗
║                  🎉 OpenCode Telegram Bot - 启动指南              ║
╚═══════════════════════════════════════════════════════════════╝

## ✅ 当前状态

- ✅ Bot Token 已验证（@your_bot_username）
- ✅ OpenCode 正在运行（端口 4096）
- ✅ Python 依赖已安装
- ✅ 代码已完成（100%）

## ⚠️ 当前问题

Bot 遇到 "Conflict" 错误，原因：
- Telegram 服务器端可能有 webhook 残留
- 或有其他客户端在连接

## 🚀 解决方案：使用 Webhook 模式

我们已创建了 `bot_webhook.py`，使用 webhook 而不是 polling。

### 第 1 步：安装 ngrok（内网穿透）

由于 webhook 需要公网 HTTPS URL，我们使用 ngrok：

```bash
# 如果没有安装，用 brew 安装
brew install ngrok
```

### 第 2 步：启动 ngrok

```bash
ngrok http 8443
```

你会看到类似输出：
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8443
```

**复制这个 HTTPS URL**（例如：`https://abc123.ngrok.io`）

### 第 3 步：更新 .env 配置

编辑 `.env` 文件，添加 webhook URL：

```bash
cd /path/to/opencode-telegram-bridge
nano .env
```

更新这一行：
```env
WEBHOOK_URL=https://your-ngrok-url.ngrok.io
```

替换为你的 ngrok URL。

### 第 4 步：启动 Webhook Bot

```bash
python3 bot_webhook.py
```

### 第 5 步：测试

1. 在 Telegram 中搜索 `@your_bot_username`
2. 发送 `/start`
3. 发送测试消息

---

## 📊 两种模式对比

| 特性 | Polling (bot.py) | Webhook (bot_webhook.py) |
|------|-------------------|------------------------|
| 速度 | 较慢（几秒延迟） | 快速（实时） |
| 资源占用 | 高（持续轮询） | 低（事件驱动） |
| 适合 | 开发/测试 | 生产环境 |
| 需要公网 IP | 否 | 是（ngrok） |
| 配置复杂度 | 简单 | 需要配置 URL |

---

## 🔧 启动流程总结

### Polling 模式（简单）
```bash
# 1. 启动 OpenCode（如果还没运行）
opencode serve --port=4096

# 2. 启动 bot
python3 bot.py
```

### Webhook 模式（推荐）
```bash
# 1. 启动 OpenCode（如果还没运行）
opencode serve --port=4096

# 2. 终端 1：启动 ngrok
ngrok http 8443
# 复制输出中的 HTTPS URL

# 3. 终端 2：更新 .env
cd /path/to/opencode-telegram-bridge
nano .env
# 更新 WEBHOOK_URL

# 4. 启动 webhook bot
python3 bot_webhook.py
```

---

## 📞 常见问题

### Q: ngrok URL 怎么获取？
A: 运行 `ngrok http 8443`，复制 "Forwarding" 行的 HTTPS URL

### Q: Webhook URL 需要什么格式？
A: `https://your-url.ngrok.io/webhook`（注意：最后不需要加 /webhook，bot 会自动处理）

### Q: Bot 不响应怎么办？
A:
1. 检查 ngrok 是否在运行
2. 检查 bot_webhook.py 日志
3. 在 Telegram 中发送 /start 重试

### Q: OpenCode 连接失败怎么办？
A:
1. 确认 OpenCode 在运行：`lsof -i :4096`
2. 测试 API：`curl http://localhost:4096/session`

### Q: ngrok 免费版够用吗？
A: 对于个人使用完全够用。免费版：
- 永久免费的 HTTPS URL
- 每个 tunnel 有速度限制
- 足够处理消息流量

---

## 🎯 推荐方案

对于生产环境，推荐使用：
- ✅ Webhook 模式（更快，资源效率更高）
- ✅ ngrok（用于开发/测试）
- ✅ 域名 + SSL（用于生产环境）

---

## 📁 项目文件

```
opencode-telegram-bridge/
├── bot.py                  # Polling 模式 bot
├── bot_webhook.py         # 🆕 Webhook 模式 bot（推荐）
├── verify_token.py          # Token 验证工具
├── start.sh               # 一键启动脚本
├── setup.sh               # 自动安装脚本
├── requirements.txt         # Python 依赖
├── .env                   # 配置文件
├── BOT_创建指南.md          # Bot 创建详细指南
├── 项目完成报告.md          # 项目完成总结
├── README.md              # 英文文档
├── 快速启动.md              # 中文快速指南
└── 启动指南.md              # 本文件
```

---

## 🚀 快速启动命令

```bash
# 方法 1：Polling 模式（简单）
cd /path/to/opencode-telegram-bridge
python3 bot.py

# 方法 2：Webhook 模式（推荐）
cd /path/to/opencode-telegram-bridge

# 终端 1
ngrok http 8443

# 终端 2（复制 ngrok URL 后）
nano .env  # 更新 WEBHOOK_URL
python3 bot_webhook.py
```

---

## ✨ 你现在可以选择：

**A. 立即使用 Polling 模式**
- ✅ 简单
- ✅ 无需 ngrok
- ⚠️  可能有冲突问题

**B. 使用 Webhook 模式（推荐）**
- ✅ 更快
- ✅ 资源效率更高
- ✅ 无冲突问题
- ⚠️  需要配置 ngrok

你想使用哪种模式？我推荐 Webhook！

---

╔═════════════════════════════════════════════════════════════╗
║                    📞 需要帮助？                              ║
║                                                              ║
║ 查看：BOT_创建指南.md（详细 Bot 创建）              ║
║      README.md（英文完整文档）                      ║
║      项目完成报告.md（项目总结）                         ║
║                                                              ║
╚═════════════════════════════════════════════════════════════════╝
