# Gemini MCP Server

一個基於 Google Gemini API 的 Model Context Protocol (MCP) 伺服器，提供多種AI功能插件。

## 功能特色

### 🎯 核心功能
- **Gemini API 整合**: 直接與 Google Gemini 模型互動
- **多輪對話支援**: 保持對話歷史和上下文
- **插件架構**: 模組化設計，易於擴展

### 📝 文本處理插件
- **智能摘要**: 自動生成文件摘要
- **多語言翻譯**: 支援多種語言間的翻譯
- **語法檢查**: 檢查和修正文本語法錯誤
- **情感分析**: 分析文本的情感傾向

### 💻 程式碼助手插件
- **程式碼生成**: 根據需求生成程式碼
- **程式碼解釋**: 解釋程式碼功能和邏輯
- **程式碼重構**: 建議程式碼改進方案
- **錯誤診斷**: 幫助診斷和修復程式碼錯誤

### 🧠 知識管理插件
- **問答系統**: 智能問答功能
- **知識搜尋**: 從大量資料中搜尋相關資訊
- **文件整理**: 自動分類和組織文件
- **學習助手**: 提供個性化學習建議

## 安裝方式

### 方法一：使用安裝腳本（推薦）

```bash
# 克隆或下載專案到本地
cd /path/to/your/project

# 執行安裝腳本
./install.sh

# 設定 API 金鑰
export GEMINI_API_KEY="your-gemini-api-key"

# 測試安裝
make demo
```

### 方法二：手動安裝

1. **建立虛擬環境**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **安裝依賴**
```bash
pip install -r requirements.txt
```

3. **設定環境變數**
```bash
cp .env.example .env
# 編輯 .env 檔案，設定你的 GEMINI_API_KEY
```

### 方法三：使用 Makefile

```bash
# 查看可用命令
make help

# 安裝依賴
make install

# 執行 demo
make demo

# 啟動伺服器
make server
```

## 使用方法

### 啟動 MCP 伺服器
```bash
gemini-mcp
```

### 配置客戶端

在你的 MCP 客戶端（如 Claude Desktop）中添加以下配置：

```json
{
  "mcpServers": {
    "gemini-mcp": {
      "command": "gemini-mcp",
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```

## 可用工具

### 基本對話
- `chat`: 與 Gemini 進行對話
- `generate`: 生成文本內容

### 文本處理
- `summarize`: 摘要文本
- `translate`: 翻譯文本
- `check_grammar`: 檢查語法
- `analyze_sentiment`: 情感分析

### 程式碼助手
- `generate_code`: 生成程式碼
- `explain_code`: 解釋程式碼
- `refactor_code`: 重構建議
- `debug_code`: 錯誤診斷

### 知識管理
- `ask_question`: 問答
- `search_knowledge`: 知識搜尋
- `organize_documents`: 文件整理
- `learning_assist`: 學習輔助

## 開發說明

### 專案結構
```
mcp_1018/
├── src/
│   └── gemini_mcp/
│       ├── __init__.py
│       ├── server.py          # 主要伺服器
│       ├── gemini_client.py   # Gemini API 客戶端
│       └── plugins/
│           ├── __init__.py
│           ├── text_processing.py
│           ├── code_assistant.py
│           └── knowledge_management.py
├── tests/
├── pyproject.toml
└── README.md
```

### 添加新插件

1. 在 `src/gemini_mcp/plugins/` 創建新的插件檔案
2. 實作插件類別並繼承基本插件類別
3. 在 `server.py` 中註冊新插件

## 授權條款

MIT License

## 貢獻指南

歡迎提交 Pull Request 和 Issue！

## 聯繫方式

如有問題請聯繫：your.email@example.com