# 📖 Telegram Bot 创建详细指南

## 步骤 1：打开 Telegram 并找到 BotFather

1. 在你的手机或电脑上打开 **Telegram** 应用
2. 在搜索框输入：`@BotFather`
3. 点击 **BotFather** (有蓝色勾的官方账号)
4. 点击 **START** 开始对话

---

## 步骤 2：创建新 Bot

1. 向 BotFather 发送命令：
   ```
   /newbot
   ```

2. BotFather 会回复：
   ```
   Alright, a new bot. How are we going to call it? Please choose a name for your bot.
   ```

3. 输入 Bot 的**显示名称**（可以是中文）：
   ```
   My OpenCode Bot
   ```

4. BotFather 会回复：
   ```
   Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
   ```

5. 输入 Bot 的**用户名**（必须是英文，以 `bot` 结尾）：
   ```
   MyOpenCodeBot
   ```

6. 如果用户名可用，BotFather 会发送成功消息：
   ```
   Done! Congratulations on your new bot. You will find it at t.me/MyOpenCodeBot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands.

   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

   Keep your token secure and store it safely, it can be used by anyone to control your bot.
   ```

---

## 步骤 3：复制 Bot Token ⭐ 重要！

1. **复制** BotFather 发送给你的 Token
2. Token 格式：`数字:35位字符串`
3. 示例：`1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

⚠️ **注意**：
- Token 长度固定：46 个字符
- 格式：`10位数字:35位字符串`
- 只能从 BotFather 获取
- 不要分享给别人

---

## 步骤 4：测试 Token

使用我们的验证脚本测试 token：

```bash
cd /path/to/opencode-telegram-bridge
python3 verify_token.py
```

如果 token 有效，你会看到：
```
✅ Token 有效！

Bot 信息：
  名称: My OpenCode Bot
  用户名: @MyOpenCodeBot
  ID: 123456789
```

如果 token 无效，你会看到：
```
❌ Token 无效！
错误: Unauthorized
```

---

## 步骤 5：配置 Bot

将你的 token 添加到 `.env` 文件：

```bash
cd /path/to/opencode-telegram-bridge
nano .env
```

找到这一行：
```
BOT_TOKEN=your_telegram_bot_token_here
```

替换为你的新 token：
```
BOT_TOKEN=你的新token
```

保存并退出（nano: Ctrl+O, Enter, Ctrl+X）

---

## 步骤 6：启动 Bot

```bash
python3 bot.py
```

看到以下输出表示成功：
```
2026-02-01 17:40:34 - __main__ - INFO - Starting Telegram bot with polling...
```

---

## 步骤 7：在 Telegram 中使用

1. 在 Telegram 中搜索你的 bot 用户名
   ```
   @MyOpenCodeBot
   ```
2. 点击 **START**
3. 发送 `/start`
4. 发送测试消息：
   ```
   你好！
   ```

---

## ❓ 常见问题

### Q: BotFather 说用户名已被占用怎么办？
A: 尝试另一个用户名，例如：
```
MyOpenCodeBot2
MyOpenCodeBot2024
MyOCBot
```

### Q: Token 丢了怎么办？
A: 不要担心，重新获取：
1. 给 BotFather 发送：`/mybots`
2. 选择你的 bot
3. 点击 **API Token**
4. Token 会重新显示

### Q: Bot 可以更改吗？
A: 可以！给 BotFather 发送：
- `/mybots` - 查看所有 bot
- `/setname` - 修改 bot 名称
- `/setdescription` - 修改描述
- `/setabouttext` - 修改关于信息

### Q: 可以删除 bot 吗？
A: 可以，给 BotFather 发送：
```
/deletebot
```
然后选择要删除的 bot

---

## 🎉 完成检查清单

- [ ] 已在 Telegram 中找到 @BotFather
- [ ] 已创建新 bot（使用 `/newbot`）
- [ ] 已设置 bot 名称和用户名
- [ ] 已从 BotFather 复制 Token
- [ ] 已使用 verify_token.py 验证 Token
- [ ] 已将 Token 添加到 `.env` 文件
- [ ] 已启动 bot（`python3 bot.py`）
- [ ] 已在 Telegram 中找到并发送消息给 bot

---

## 📞 需要帮助？

如果遇到问题：
1. 查看 BotFather 的帮助：`/help`
2. 查看 Telegram Bot API 文档：https://core.telegram.org/bots
3. 查看我们的 GitHub issues

祝你使用愉快！🚀
