#!/bin/bash
# 互動式 MCP 工具選單

API_BASE="http://127.0.0.1:8000"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 檢查 API 狀態
check_api() {
    if curl -s "$API_BASE/" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API 服務正在運行${NC}"
        return 0
    else
        echo -e "${RED}❌ API 服務未運行，請先啟動服務器${NC}"
        echo -e "${YELLOW}啟動命令：${NC}"
        echo "source .venv/bin/activate && export GEMINI_API_KEY='您的API金鑰' && python http_api_server.py"
        return 1
    fi
}

# 調用工具的通用函數
call_tool() {
    local tool_name="$1"
    local arguments="$2"
    
    echo -e "${CYAN}🔄 調用工具: $tool_name${NC}"
    
    local response=$(curl -s -X POST "$API_BASE/tool" \
        -H "Content-Type: application/json" \
        -d "{\"tool_name\": \"$tool_name\", \"arguments\": $arguments}")
    
    local success=$(echo "$response" | python -c "import sys, json; print(json.load(sys.stdin).get('success', False))")
    
    if [ "$success" = "True" ]; then
        echo -e "${GREEN}✅ 成功${NC}"
        echo "$response" | python -c "import sys, json; print(json.load(sys.stdin)['data'])"
    else
        echo -e "${RED}❌ 失敗${NC}"
        echo "$response" | python -c "import sys, json; print(json.load(sys.stdin).get('error', '未知錯誤'))"
    fi
}

# 顯示主選單
show_menu() {
    clear
    echo -e "${PURPLE}🤖 Gemini MCP 工具選單${NC}"
    echo "=================================="
    echo -e "${CYAN}1.${NC} 💬 翻譯文本"
    echo -e "${CYAN}2.${NC} 💻 生成程式碼"
    echo -e "${CYAN}3.${NC} 📝 文本摘要"
    echo -e "${CYAN}4.${NC} 🔍 程式碼審查"
    echo -e "${CYAN}5.${NC} 🧠 智能問答"
    echo -e "${CYAN}6.${NC} 😊 情感分析"
    echo -e "${CYAN}7.${NC} 🔧 程式碼解釋"
    echo -e "${CYAN}8.${NC} 📊 查看可用工具"
    echo -e "${CYAN}9.${NC} ❓ 系統狀態"
    echo -e "${CYAN}0.${NC} 🚪 退出"
    echo "=================================="
}

# 翻譯功能
translate_function() {
    echo -e "${YELLOW}請輸入要翻譯的文本：${NC}"
    read -r text
    echo -e "${YELLOW}目標語言 (預設: zh-tw)：${NC}"
    read -r lang
    lang=${lang:-zh-tw}
    
    call_tool "translate" "{\"text\": \"$text\", \"target_language\": \"$lang\"}"
}

# 程式碼生成
code_generation() {
    echo -e "${YELLOW}請描述您想要的程式碼：${NC}"
    read -r description
    echo -e "${YELLOW}程式語言 (預設: python)：${NC}"
    read -r language
    language=${language:-python}
    
    call_tool "generate_code" "{\"description\": \"$description\", \"language\": \"$language\"}"
}

# 文本摘要
text_summary() {
    echo -e "${YELLOW}請輸入要摘要的文本：${NC}"
    read -r text
    
    call_tool "summarize" "{\"text\": \"$text\"}"
}

# 程式碼審查
code_review() {
    echo -e "${YELLOW}請輸入要審查的程式碼：${NC}"
    read -r code
    echo -e "${YELLOW}程式語言 (預設: python)：${NC}"
    read -r language
    language=${language:-python}
    
    call_tool "code_review" "{\"code\": \"$code\", \"language\": \"$language\"}"
}

# 智能問答
ask_question() {
    echo -e "${YELLOW}請輸入您的問題：${NC}"
    read -r question
    
    call_tool "ask_question" "{\"question\": \"$question\"}"
}

# 情感分析
sentiment_analysis() {
    echo -e "${YELLOW}請輸入要分析的文本：${NC}"
    read -r text
    
    call_tool "analyze_sentiment" "{\"text\": \"$text\"}"
}

# 程式碼解釋
explain_code() {
    echo -e "${YELLOW}請輸入要解釋的程式碼：${NC}"
    read -r code
    echo -e "${YELLOW}程式語言 (預設: python)：${NC}"
    read -r language
    language=${language:-python}
    
    call_tool "explain_code" "{\"code\": \"$code\", \"language\": \"$language\"}"
}

# 查看可用工具
show_tools() {
    echo -e "${CYAN}📊 可用工具列表：${NC}"
    curl -s "$API_BASE/tools" | python -m json.tool
}

# 主循環
main() {
    # 檢查 API 狀態
    if ! check_api; then
        exit 1
    fi
    
    while true; do
        show_menu
        echo -ne "${YELLOW}請選擇功能 (0-9): ${NC}"
        read -r choice
        
        case $choice in
            1) translate_function ;;
            2) code_generation ;;
            3) text_summary ;;
            4) code_review ;;
            5) ask_question ;;
            6) sentiment_analysis ;;
            7) explain_code ;;
            8) show_tools ;;
            9) check_api ;;
            0) echo -e "${GREEN}👋 再見！${NC}"; exit 0 ;;
            *) echo -e "${RED}❌ 無效選擇，請重試${NC}" ;;
        esac
        
        echo -e "\n${YELLOW}按 Enter 鍵繼續...${NC}"
        read -r
    done
}

# 執行主程式
main