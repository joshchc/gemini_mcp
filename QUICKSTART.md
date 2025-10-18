# Gemini MCP Server 快速開始指南

## 🚀 快速開始

### 1. 環境設置

確保你有 Python 3.8+ 環境：

```bash
# 檢查 Python 版本
python --version

# 進入專案目錄
cd /Users/hc/mcp_1018

# 啟用虛擬環境
source .venv/bin/activate
```

### 2. 設置 API 金鑰

設置你的 Gemini API 金鑰：

```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

### 3. 快速測試

執行 demo 腳本來測試基本功能：

```bash
python demo.py
```

如果看到以下輸出，表示設置成功：
```
🚀 Gemini MCP Server Demo
==================================================
🔧 Initializing Gemini client...
✅ Client initialized successfully!
💬 Testing basic conversation...
📝 Testing text summarization...
💻 Testing code generation...
🎉 Demo completed successfully!
```

## 🛠️ 可用功能

### 核心對話功能
- **chat**: 多輪對話
- **generate**: 單次內容生成
- **reset_chat**: 重置對話歷史

### 📝 文本處理插件
- **summarize**: 文本摘要
- **translate**: 多語言翻譯
- **check_grammar**: 語法檢查
- **analyze_sentiment**: 情感分析
- **extract_keywords**: 關鍵詞提取
- **rewrite_text**: 文本重寫

### 💻 程式碼助手插件
- **generate_code**: 程式碼生成
- **explain_code**: 程式碼解釋
- **refactor_code**: 重構建議
- **debug_code**: 錯誤診斷
- **optimize_code**: 效能優化
- **code_review**: 程式碼審查
- **generate_tests**: 生成測試

### 🧠 知識管理插件
- **ask_question**: 智能問答
- **search_knowledge**: 知識搜尋
- **organize_information**: 資訊整理
- **create_study_plan**: 學習計劃
- **research_topic**: 主題研究
- **compare_concepts**: 概念比較
- **explain_concept**: 概念解釋

## 🔧 MCP 客戶端配置

如果你要在 MCP 客戶端（如 Claude Desktop）中使用這個伺服器：

1. 編輯你的 MCP 客戶端配置檔案
2. 添加以下配置：

```json
{
  "mcpServers": {
    "gemini-mcp": {
      "command": "python",
      "args": ["/Users/hc/mcp_1018/run_server.py"],
      "env": {
        "GEMINI_API_KEY": "your-gemini-api-key-here"
      }
    }
  }
}
```

## 📁 專案結構

```
mcp_1018/
├── src/
│   └── gemini_mcp/
│       ├── __init__.py           # 套件初始化
│       ├── server.py             # 主要 MCP 伺服器
│       ├── gemini_client.py      # Gemini API 客戶端
│       ├── config.py             # 配置管理
│       └── plugins/              # 插件目錄
│           ├── __init__.py
│           ├── base.py           # 基礎插件類別
│           ├── text_processing.py    # 文本處理插件
│           ├── code_assistant.py     # 程式碼助手插件
│           └── knowledge_management.py  # 知識管理插件
├── tests/
│   └── test_basic.py             # 基本測試
├── demo.py                       # 示範腳本
├── run_server.py                 # 伺服器啟動腳本
├── pyproject.toml                # 專案配置
├── README.md                     # 專案說明
├── .env.example                  # 環境變數範例
└── mcp_client_config.json        # MCP 客戶端配置範例
```

## 🔍 故障排除

### 問題：ModuleNotFoundError
**解決方案**：確保虛擬環境已啟用且套件已安裝
```bash
source .venv/bin/activate
pip install mcp google-generativeai
```

### 問題：API 金鑰錯誤
**解決方案**：檢查環境變數設置
```bash
echo $GEMINI_API_KEY
export GEMINI_API_KEY="your-actual-api-key"
```

### 問題：模型不支援
**解決方案**：使用支援的模型名稱
```bash
export GEMINI_MODEL="gemini-2.5-flash"
```

## 🎯 下一步

1. **自定義插件**：根據需求創建新的插件
2. **效能調整**：調整溫度、最大 tokens 等參數
3. **安全強化**：實作更嚴格的輸入驗證
4. **監控日誌**：添加詳細的執行日誌
5. **擴展功能**：整合更多外部 API 和服務

## 📞 支援

如有問題，請檢查：
1. API 金鑰是否正確設置
2. 網路連接是否正常
3. Python 環境是否完整
4. 套件版本是否相容

祝你使用愉快！🎉