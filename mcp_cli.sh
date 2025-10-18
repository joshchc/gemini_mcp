#!/bin/bash
# Gemini MCP 工具使用腳本

API_BASE="http://127.0.0.1:8000"

# 檢查 API 狀態
check_status() {
    echo "🔍 檢查 API 狀態..."
    curl -s "$API_BASE/" | python -m json.tool
}

# 翻譯文本
translate_text() {
    local text="$1"
    local lang="${2:-zh-tw}"
    echo "🔄 翻譯: $text"
    curl -s -X POST "$API_BASE/tool" \
        -H "Content-Type: application/json" \
        -d "{\"tool_name\": \"translate\", \"arguments\": {\"text\": \"$text\", \"target_language\": \"$lang\"}}" \
        | python -c "import sys, json; data=json.load(sys.stdin); print('翻譯結果:', data['data'])"
}

# 生成程式碼
generate_code() {
    local description="$1"
    local language="${2:-python}"
    echo "💻 生成程式碼: $description"
    curl -s -X POST "$API_BASE/tool" \
        -H "Content-Type: application/json" \
        -d "{\"tool_name\": \"generate_code\", \"arguments\": {\"description\": \"$description\", \"language\": \"$language\"}}" \
        | python -c "import sys, json; data=json.load(sys.stdin); print('生成的程式碼:'); print(data['data'])"
}

# 文本摘要
summarize_text() {
    local text="$1"
    echo "📝 文本摘要..."
    curl -s -X POST "$API_BASE/tool" \
        -H "Content-Type: application/json" \
        -d "{\"tool_name\": \"summarize\", \"arguments\": {\"text\": \"$text\"}}" \
        | python -c "import sys, json; data=json.load(sys.stdin); print('摘要結果:', data['data'])"
}

# 顯示幫助
show_help() {
    echo "🤖 Gemini MCP 工具使用指南"
    echo "================================"
    echo "check_status              - 檢查 API 狀態"
    echo "translate_text '文本' [語言] - 翻譯文本"
    echo "generate_code '描述' [語言] - 生成程式碼"
    echo "summarize_text '文本'     - 文本摘要"
    echo ""
    echo "範例:"
    echo "  translate_text 'Hello World' zh-tw"
    echo "  generate_code '創建一個 Flask 應用' python"
    echo "  summarize_text '長篇文章內容...'"
}

# 根據參數執行對應功能
case "$1" in
    "status")
        check_status
        ;;
    "translate")
        translate_text "$2" "$3"
        ;;
    "code")
        generate_code "$2" "$3"
        ;;
    "summarize")
        summarize_text "$2"
        ;;
    "help"|"")
        show_help
        ;;
    *)
        echo "❌ 未知命令: $1"
        show_help
        ;;
esac