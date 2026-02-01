#!/usr/bin/env python3
"""
Interactive Telegram Bot Creation Guide
Helps you create a Telegram bot and configure the bridge
"""

import re


def print_header():
    print("\n" + "=" * 60)
    print("  🤖 Telegram Bot 创建向导")
    print("=" * 60)
    print()


def print_step(step_num, title):
    print(f"\n{'=' * 60}")
    print(f"  步骤 {step_num}: {title}")
    print("=" * 60)
    print()


def print_success(msg):
    print(f"  ✅ {msg}")


def print_info(msg):
    print(f"  ℹ️  {msg}")


def print_warning(msg):
    print(f"  ⚠️  {msg}")


def print_error(msg):
    print(f"  ❌ {msg}")


def validate_bot_token(token):
    """Validate Telegram Bot Token format"""
    # Telegram bot tokens are like: 123456:ABCdefGHIjklMNOpqrsTUVwxyz
    pattern = r"^\d+:[A-Za-z0-9_-]{35}$"
    return bool(re.match(pattern, token))


def main():
    print_header()

    # Step 1: Open Telegram and find BotFather
    print_step(1, "在 Telegram 中找到 BotFather")
    print_info("打开 Telegram 应用")
    print_info("搜索: @BotFather")
    print_info("点击开始聊天")
    print()

    input("  📝 完成后按 Enter 继续...")

    # Step 2: Create new bot
    print_step(2, "创建新的 Bot")
    print_info("向 @BotFather 发送命令:")
    print_info("  /newbot")
    print()
    print_warning("BotFather 会要求你:")
    print("    1. 为 Bot 设置名称（例如: My OpenCode Bot）")
    print("    2. 设置用户名（必须以 'bot' 结尾，例如: MyOpenCodeBot）")
    print()

    input("  📝 完成后按 Enter 继续...")

    # Step 3: Get the token
    print_step(3, "获取 Bot Token")
    print_warning("BotFather 会发送给你一个消息，包含:")
    print("    ✅ Bot 的用户名（例如 @MyOpenCodeBot）")
    print("    ✅ API Token（类似: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz）")
    print()
    print_info("🔑 **这个 Token 非常重要！**")
    print("    请复制这个 Token，你会需要它来配置桥接服务")
    print()

    input("  📝 找到 Token 后按 Enter 继续...")

    # Step 4: Input the token
    print_step(4, "配置 Bot Token")
    print()
    while True:
        token = input("  🔑 请粘贴你的 Bot Token: ").strip()

        if not token:
            print_error("Token 不能为空！")
            continue

        if validate_bot_token(token):
            print_success("Token 格式正确！")
            break
        else:
            print_warning("Token 格式看起来不正确，但继续尝试...")
            print_info("正确格式应该是: 数字:35位字符串")
            confirm = input("  是否继续？(y/n): ").lower()
            if confirm != "y":
                continue
            break

    # Step 5: Save to .env
    print_step(5, "保存配置")
    print()

    env_content = f"""# Telegram Bot Configuration
BOT_TOKEN={token}

# OpenCode Configuration
OPENCODE_URL=http://localhost:4096

# Webhook Configuration
WEBHOOK_URL=https://your-ngrok-url.ngrok.io
WEBHOOK_SECRET=random_secret_token_for_validation
PORT=8443
"""

    import os

    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

    print_info(f"保存到: {env_path}")

    try:
        with open(env_path, "w") as f:
            f.write(env_content)
        print_success("配置已保存！")
    except Exception as e:
        print_error(f"保存失败: {e}")
        print_info("请手动创建 .env 文件并添加以下内容:")
        print("-" * 60)
        print(env_content)
        print("-" * 60)
        return False

    # Step 6: Verify
    print_step(6, "验证配置")

    try:
        with open(env_path, "r") as f:
            content = f.read()
            if token in content:
                print_success("Token 已正确保存到 .env 文件")
            else:
                print_error("Token 未正确保存")
                return False
    except Exception as e:
        print_error(f"验证失败: {e}")
        return False

    # Step 7: Final summary
    print("\n" + "=" * 60)
    print("  🎉 配置完成！")
    print("=" * 60)
    print()
    print_success("你已完成所有配置步骤！")
    print()
    print_info("下一步:")
    print("  1. 确保OpenCode正在运行:")
    print("     opencode serve --port=4096")
    print()
    print("  2. 安装 Python 依赖:")
    print("     cd /path/to/opencode-telegram-bridge")
    print("     pip3 install -r requirements.txt")
    print()
    print("  3. 启动 Bot:")
    print("     python3 bot.py")
    print()
    print("  4. 在 Telegram 中找到你的 bot 并发送 /start")
    print()
    print_info("📚 更多信息请查看:")
    print("     - README.md (英文完整文档)")
    print("     - 快速启动.md (中文快速指南)")
    print()
    print("=" * 60)

    return True


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ 操作已取消")
        exit(1)
