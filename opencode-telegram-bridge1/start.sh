#!/bin/bash

# One-Command Setup Script for OpenCode Telegram Bridge

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

clear
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🤖 OpenCode + Telegram Bridge - 一键启动向导              ║
║                                                               ║
║    让你的 OpenCode 通过 Telegram 随时可用                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF

# Step 1: Check Python
print_step "步骤 1: 检查 Python 环境"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python 已安装: $PYTHON_VERSION"
else
    print_error "Python 3 未安装！请先安装 Python 3.10+"
    exit 1
fi

# Step 2: Check OpenCode
print_step "步骤 2: 检查 OpenCode 服务器"
if lsof -i :4096 > /dev/null 2>&1; then
    print_success "OpenCode 正在运行 (端口 4096)"
else
    print_warning "OpenCode 未运行，正在启动..."
    opencode serve --port=4096 > /tmp/opencode.log 2>&1 &
    sleep 3

    if lsof -i :4096 > /dev/null 2>&1; then
        print_success "OpenCode 已成功启动"
    else
        print_error "OpenCode 启动失败"
        echo "请手动启动: opencode serve --port=4096"
        exit 1
    fi
fi

# Step 3: Install dependencies
print_step "步骤 3: 安装 Python 依赖"
print_info "正在安装依赖包..."
pip3 install -r requirements.txt --quiet
print_success "依赖安装完成"

# Step 4: Setup Bot
print_step "步骤 4: 配置 Telegram Bot"
if [ -f .env ]; then
    if grep -q "your_telegram_bot_token_here" .env; then
        print_warning ".env 已存在但未配置 Bot Token"
        print_info "运行交互式配置向导..."
        python3 create_bot.py || exit 1
    else
        print_success "Bot Token 已配置"
        BOT_NAME=$(grep "BOT_TOKEN" .env | cut -d'=' -f2 | cut -c1-20)
        print_info "Token 前缀: $BOT_NAME..."
    fi
else
    print_info ".env 文件不存在，运行交互式配置向导..."
    python3 create_bot.py || exit 1
fi

# Step 5: Test connection
print_step "步骤 5: 测试连接"
print_info "测试 OpenCode API..."
if curl -s http://localhost:4096/session > /dev/null 2>&1; then
    print_success "OpenCode API 可访问"
else
    print_error "无法连接到 OpenCode"
    exit 1
fi

# Step 6: Start Bot
print_step "步骤 6: 启动 Telegram Bot"
print_info "正在启动 Bot..."
echo ""
print_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_success "启动命令: python3 bot.py"
print_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
print_warning "Bot 运行中... 按 Ctrl+C 停止"
echo ""
print_info "现在可以在 Telegram 中与你的 Bot 交互了！"
echo ""
print_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the bot
python3 bot.py
