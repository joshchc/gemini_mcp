# Claude Desktop MCP 整合指南

## 📋 設定步驟

### 1. 找到 Claude Desktop 配置檔案

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%\Claude\claude_desktop_config.json
```

### 2. 編輯配置檔案

將以下內容添加到配置檔案中：

```json
{
  "mcpServers": {
    "gemini-mcp": {
      "command": "python",
      "args": ["/Users/hc/mcp_1018/simple_server.py"],
      "cwd": "/Users/hc/mcp_1018",
      "env": {
        "GEMINI_API_KEY": "your-gemini-api-key"
      }
    }
  }
}
```

### 3. 重啟 Claude Desktop

配置完成後重啟 Claude Desktop，你將可以使用以下功能：

- **聊天對話** - 與 Gemini 進行多輪對話
- **文本處理** - 摘要、翻譯、語法檢查
- **程式碼助手** - 生成、解釋、重構程式碼  
- **知識管理** - 問答、研究、學習計劃

## 🛠️ 可用工具

### 基本對話
- `chat` - 與 Gemini 對話
- `generate` - 生成內容
- `reset_chat` - 重置對話

### 文本處理
- `summarize` - 文本摘要
- `translate` - 翻譯
- `check_grammar` - 語法檢查
- `analyze_sentiment` - 情感分析
- `extract_keywords` - 關鍵詞提取
- `rewrite_text` - 文本重寫

### 程式碼助手
- `generate_code` - 程式碼生成
- `explain_code` - 程式碼解釋
- `refactor_code` - 重構建議
- `debug_code` - 錯誤診斷
- `optimize_code` - 效能優化
- `code_review` - 程式碼審查
- `generate_tests` - 測試生成

### 知識管理
- `ask_question` - 智能問答
- `search_knowledge` - 知識搜尋
- `organize_information` - 資訊整理
- `create_study_plan` - 學習計劃
- `research_topic` - 主題研究
- `compare_concepts` - 概念比較
- `explain_concept` - 概念解釋

## 💡 使用範例

在 Claude Desktop 中，你可以這樣使用：

1. **生成程式碼：**
   "請使用 generate_code 工具幫我創建一個 Python 函數來計算費波納契數列"

2. **文本摘要：**
   "請使用 summarize 工具為這段文字做摘要：[你的文字]"

3. **程式碼解釋：**
   "請使用 explain_code 工具解釋這段程式碼：[你的程式碼]"

## 🔧 故障排除

### 問題：Claude 找不到 MCP 工具
**解決方案：**
1. 確認配置檔案格式正確
2. 重啟 Claude Desktop
3. 檢查伺服器路徑是否正確

### 問題：工具執行失敗
**解決方案：**
1. 檢查 API 金鑰是否正確
2. 確認 Python 環境可用
3. 查看 MCP 伺服器日誌

### 問題：權限錯誤
**解決方案：**
1. 確認 Python 腳本有執行權限
2. 檢查檔案路徑訪問權限