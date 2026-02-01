#!/usr/bin/env python3
"""
Telegram Bot Token Verification Script
Validates your bot token and shows bot information
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def verify_token(token: str) -> bool:
    """Verify if token is valid"""
    try:
        import httpx

        print("🔍 正在验证 Token...")
        print()

        response = httpx.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
        data = response.json()

        if data.get("ok"):
            bot_info = data.get("result", {})
            print("✅ Token 有效！")
            print()
            print("🤖 Bot 信息：")
            print(f"  名称: {bot_info.get('first_name', 'N/A')}")
            print(f"  用户名: @{bot_info.get('username', 'N/A')}")
            print(f"  Bot ID: {bot_info.get('id', 'N/A')}")
            print(
                f"  是否支持群组: {'是' if bot_info.get('can_join_groups') else '否'}"
            )
            print(
                f"  是否支持内联: {'是' if bot_info.get('supports_inline_queries') else '否'}"
            )
            print()
            print("📞 可以通过以下方式访问你的 Bot:")
            print(f"  https://t.me/{bot_info.get('username', '')}")
            print()
            return True
        else:
            print("❌ Token 无效！")
            print()
            print(f"错误代码: {data.get('error_code', 'Unknown')}")
            print(f"错误描述: {data.get('description', 'Unknown error')}")
            print()

            # Provide specific advice based on error
            error_code = data.get("error_code")
            if error_code == 401:
                print("💡 常见原因:")
                print("   - Token 已过期")
                print("   - Token 不正确（请检查是否复制完整）")
                print("   - Bot 已被删除")
                print()
                print("🔧 解决方案:")
                print("   1. 在 Telegram 中打开 @BotFather")
                print("   2. 发送 /mybots")
                print("   3. 选择你的 bot")
                print("   4. 点击 'API Token' 获取新 token")
            elif error_code == 404:
                print("💡 原因: Bot 不存在")
                print()
                print("🔧 解决方案: 重新创建 bot")
                print("   1. 给 BotFather 发送 /newbot")
                print("   2. 按提示创建新 bot")

            print()
            return False

    except Exception as e:
        print(f"❌ 验证失败: {e}")
        print()
        print("💡 可能的原因:")
        print("   - 网络连接问题")
        print("   - Telegram API 暂时不可用")
        print("   - Token 格式不正确")
        print()
        return False


def check_env_token():
    """Check if token is set in .env"""
    print("=" * 60)
    print("  📋 检查 .env 文件中的 Token")
    print("=" * 60)
    print()

    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

    if not os.path.exists(env_file):
        print("⚠️  .env 文件不存在")
        print("   请先运行: cp .env.example .env")
        return None

    from dotenv import dotenv_values

    config = dotenv_values(env_file)
    token = config.get("BOT_TOKEN", "").strip()

    if not token:
        print("⚠️  BOT_TOKEN 未在 .env 中设置")
        print()
        print("📝 请编辑 .env 文件:")
        print(f"   nano {env_file}")
        print()
        print("然后添加你的 BOT_TOKEN:")
        print("   BOT_TOKEN=你的token")
        return None

    if token == "your_telegram_bot_token_here":
        print("⚠️  BOT_TOKEN 使用的是示例值")
        print("   请替换为你从 @BotFather 获取的真实 token")
        return None

    # Show token preview (first 10 chars)
    preview = token[:10] + "..." if len(token) > 10 else token
    print(f"✅ 在 .env 中找到 Token")
    print(f"   Token 前缀: {preview}")
    print()

    return token


def main():
    print("\n" + "=" * 60)
    print("  🤖 Telegram Bot Token 验证工具")
    print("=" * 60)
    print()

    # Option 1: Token provided as argument
    if len(sys.argv) > 1:
        token = sys.argv[1]
        print(f"📝 使用命令行参数提供的 Token")
        print(f"   Token 前缀: {token[:10]}...")
        print()
        valid = verify_token(token)
        return 0 if valid else 1

    # Option 2: Check .env file
    token = check_env_token()

    if not token:
        print()
        print("=" * 60)
        print("  使用方法:")
        print("=" * 60)
        print()
        print("1. 验证命令行参数中的 Token:")
        print("   python3 verify_token.py YOUR_BOT_TOKEN")
        print()
        print("2. 验证 .env 文件中的 Token:")
        print("   python3 verify_token.py")
        print()
        print("3. 获取新 Token（在 Telegram 中）:")
        print("   - 打开 @BotFather")
        print("   - 发送 /newbot")
        print("   - 按提示创建 bot")
        print("   - 复制 Token")
        print()
        print("📚 详细指南: 查看 BOT_创建指南.md")
        print()
        return 1

    print("=" * 60)
    print("  🔍 开始验证")
    print("=" * 60)
    print()

    valid = verify_token(token)

    if valid:
        print("🎉 恭喜！Token 验证通过！")
        print()
        print("📖 下一步:")
        print("   1. 确保 OpenCode 正在运行:")
        print("      opencode serve --port=4096")
        print()
        print("   2. 启动 Bot:")
        print("      python3 bot.py")
        print()
        print("   3. 在 Telegram 中找到你的 bot 并发送消息")
        print()

    return 0 if valid else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ 操作已取消")
        sys.exit(1)
