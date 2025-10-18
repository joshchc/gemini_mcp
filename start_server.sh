#!/bin/bash
# 啟動 Gemini MCP 服務器的便利腳本

echo "🚀 啟動 Gemini MCP 服務器..."

# 檢查 .env 文件是否存在
if [ ! -f ".env" ]; then
    echo "❌ 找不到 .env 文件"
    echo "請創建 .env 文件並設置 GEMINI_API_KEY"
    echo "範例："
    echo "GEMINI_API_KEY=your_api_key_here"
    exit 1
fi

# 檢查虛擬環境
if [ ! -d ".venv" ]; then
    echo "❌ 找不到虛擬環境"
    echo "請先創建虛擬環境："
    echo "python -m venv .venv"
    exit 1
fi

# 激活虛擬環境
echo "📦 激活虛擬環境..."
source .venv/bin/activate

# 檢查是否有必要的依賴
echo "🔍 檢查依賴..."
python -c "import dotenv, fastapi, uvicorn, google.generativeai" 2>/dev/null || {
    echo "📥 安裝依賴..."
    pip install -r requirements.txt
}

# 啟動服務器
echo "🌟 啟動 HTTP API 服務器..."
python http_api_server.py