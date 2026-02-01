# 📋 快速启动指南

## 当前状态

✅ OpenCode 服务器已启动（端口 4096）
✅ Bot 桥接代码已完成
✅ 已创建测试脚本验证 OpenCode API
⚠️  需要你获取 Telegram Bot Token

## 🚀 开始使用

### 第一步：创建 Telegram Bot

1. 打开 Telegram
2. 搜索 `@BotFather`
3. 发送 `/newbot`
4. 按照提示设置 bot：
   - 名称：例如 "My OpenCode Bot"
   - 用户名：必须以 `bot` 结尾，例如 "MyOpenCodeBot"
5. **复制 Bot Token**（格式：`123456:ABCdefGHI...`）

### 第二步：配置环境变量

```bash
cd /path/to/opencode-telegram-bridge

# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，添加你的 Bot Token
nano .env
```

在 `.env` 中替换：
```env
BOT_TOKEN=your_actual_bot_token_here  # 改成你的真实 token
OPENCODE_URL=http://localhost:4096
```

### 第三步：安装依赖

```bash
pip3 install -r requirements.txt
```

### 第四步：启动 Bot

```bash
python3 bot.py
```

看到类似输出表示成功：
```
INFO - Starting Telegram bot with polling...
```

### 第五步：在 Telegram 中测试

1. 打开 Telegram
2. 搜索你的 bot 名称
3. 点击开始
4. 发送 `/start`
5. 发送消息，例如：`帮我分析这个项目的代码`

## 📁 项目结构

```
opencode-telegram-bridge/
├── bot.py              # 主程序
├── test_opencode.py    # 测试脚本（验证 OpenCode）
├── setup.sh           # 自动安装脚本
├── requirements.txt    # Python 依赖
├── .env.example       # 环境变量模板
├── README.md          # 详细文档
└── 快速启动.md        # 本文件（中文快速指南）
```

## 🔧 使用技巧

### Bot 命令

- `/start` - 显示欢迎信息
- `/help` - 显示帮助
- `/reset` - 重置会话（创建新的 OpenCode session）

### 发送消息

直接发送任何文本消息即可。Bot 会：
1. 将消息转发给 OpenCode
2. 等待 OpenCode 处理
3. 将结果回复给你

### 持久会话

每个用户有独立的 OpenCode session。发送 `/reset` 可以开始新会话。

## ⚠️ 注意事项

1. **响应速度**：OpenCode 处理可能需要几秒到几分钟
2. **消息长度**：超过 4000 字符会被截断
3. **会话管理**：长时间不用可能会创建多个 session
4. **OpenCode 必须运行**：确保 OpenCode 在后台运行

## 🐛 故障排除

### Bot 没有响应

```bash
# 检查 OpenCode 是否运行
lsof -i :4096

# 查看日志
tail -f /tmp/opencode.log
```

### 连接错误

```bash
# 测试 OpenCode API
curl http://localhost:4096/session
```

### Token 错误

检查 `.env` 中的 `BOT_TOKEN` 是否正确。

## 📖 更多信息

查看完整文档：`README.md`
