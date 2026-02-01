#!/bin/bash

# OpenCode 和 Bot 管理脚本
# 用于同时管理 OpenCode 和 Telegram Bot

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

OPENCODE_PID_FILE="/tmp/opencode.pid"

print_step() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
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

# 检查 OpenCode 是否在运行
check_opencode() {
    if lsof -i :4096 > /dev/null 2>&1; then
        return 0
    else
        return 1
}

# 启动 OpenCode
start_opencode() {
    print_step "启动 OpenCode 服务器"
    
    if check_opencode; then
        print_success "OpenCode 已经在运行"
        return 0
    fi
    
    print_info "正在启动 OpenCode..."
    
    # 使用 nohup 在后台启动
    nohup opencode serve --port=4096 > /tmp/opencode.log 2>&1 &
    OPENCODE_PID=$!
    
    # 保存 PID
    echo $OPENCODE_PID > "$OPENCODE_PID_FILE"
    
    # 等待启动
    sleep 5
    
    # 验证
    if check_opencode; then
        print_success "OpenCode 启动成功"
        print_info "  PID: $OPENCODE_PID"
        print_info "  地址: http://localhost:4096"
        print_info "  日志: /tmp/opencode.log"
        return 0
    else
        print_error "OpenCode 启动失败"
        print_info "查看日志: tail -f /tmp/opencode.log"
        return 1
    fi
}

# 停止 OpenCode
stop_opencode() {
    print_step "停止 OpenCode 服务器"
    
    # 检查是否有保存的 PID
    if [ -f "$OPENCODE_PID_FILE" ]; then
        SAVED_PID=$(cat "$OPENCODE_PID_FILE")
        if ps -p "$SAVED_PID" > /dev/null 2>&1; then
            print_info "正在停止 OpenCode (PID: $SAVED_PID)..."
            kill "$SAVED_PID"
            sleep 2
            print_success "OpenCode 已停止"
            rm "$OPENCODE_PID_FILE"
            return 0
        fi
    fi
    
    # 通过进程名停止
    print_info "正在查找 OpenCode 进程..."
    if pgrep -f "opencode.*serve" > /dev/null; then
        print_info "找到 OpenCode 进程，正在停止..."
        pkill -f "opencode.*serve"
        sleep 2
        print_success "OpenCode 已停止"
        return 0
    else
        print_warning "未找到运行中的 OpenCode 进程"
        return 1
    fi
}

# 检查 OpenCode 状态
status_opencode() {
    print_step "检查 OpenCode 状态"
    
    if check_opencode; then
        print_success "OpenCode 正在运行"
        
        # 显示详细信息
        PID=$(lsof -i :4096 -t -P | head -1 | awk '{print $2}')
        print_info "  端口: 4096"
        print_info "  PID: $PID"
        print_info "  地址: http://localhost:4096"
        
        # 测试连接
        if curl -s http://localhost:4096/session > /dev/null 2>&1; then
            print_success "  API 连接正常"
        else
            print_warning "  API 无响应"
        fi
        return 0
    else
        print_warning "OpenCode 未运行"
        return 1
    fi
}

# 显示 OpenCode 日志
logs_opencode() {
    if [ -f "/tmp/opencode.log" ]; then
        print_info "OpenCode 日志（最后 50 行）："
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        tail -50 /tmp/opencode.log
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        print_info "查看完整日志: tail -f /tmp/opencode.log"
    else
        print_warning "OpenCode 日志文件不存在"
    fi
}

# 显示菜单
show_menu() {
    cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║              OpenCode 管理脚本                                ║
║                                                               ║
╚═════════════════════════════════════════════════════════════╝

可用命令:

  1. 启动 OpenCode
     启动 OpenCode 服务器（后台运行）

  2. 停止 OpenCode
     停止 OpenCode 服务器

  3. 检查状态
     检查 OpenCode 运行状态

  4. 查看日志
     显示 OpenCode 日志

  5. 测试 API
     测试 OpenCode API 连接

  6. 退出
     退出此脚本

EOF
}

# 主函数
main() {
    clear
    show_menu
    
    while true; do
        echo ""
        echo -n "${BLUE}请选择操作 (1-6): ${NC}"
        read -r choice
        
        case $choice in
            1)
                start_opencode
                ;;
            2)
                stop_opencode
                ;;
            3)
                status_opencode
                ;;
            4)
                logs_opencode
                ;;
            5)
                print_info "测试 OpenCode API..."
                if curl -s http://localhost:4096/session > /dev/null 2>&1; then
                    print_success "OpenCode API 可访问"
                    curl -s http://localhost:4096/session | python3 -m json.tool | head -10
                else
                    print_error "无法连接到 OpenCode"
                fi
                ;;
            6|q|Q)
                print_info "退出..."
                exit 0
                ;;
            *)
                print_error "无效的选择，请重试"
                ;;
        esac
        
        echo ""
        echo -n "${BLUE}按 Enter 返回菜单...${NC}"
        read
    done
}

if __name__ == "__main__"; then
    main
fi
