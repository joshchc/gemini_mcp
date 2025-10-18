# GitHub Copilot 整合指南

## 🔗 整合方案總覽

我們提供了多種方式將 Gemini MCP 整合到你的開發工作流程中：

### 1. 🎯 VS Code Extension (推薦)

**特點：**
- 直接整合到 VS Code
- 右鍵選單功能
- 命令面板支援
- 自動啟動 MCP 伺服器

**安裝步驟：**
```bash
cd /Users/hc/mcp_1018/vscode-extension
npm install
npm run compile
```

**使用方式：**
- 在 VS Code 中選擇程式碼，右鍵選擇「Explain Selected Code」
- 使用 `Ctrl+Shift+P` 打開命令面板，搜尋「Gemini」
- 自動程式碼生成和重構建議

### 2. 🤖 Claude Desktop MCP

**特點：**
- 與 Claude Desktop 原生整合
- 支援所有 22 個工具
- 自然語言介面

**設定方式：**
編輯 `~/Library/Application Support/Claude/claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "gemini-mcp": {
      "command": "python",
      "args": ["/Users/hc/mcp_1018/simple_server.py"],
      "cwd": "/Users/hc/mcp_1018",
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```

### 3. 🌐 HTTP API 服務

**特點：**
- RESTful API 介面
- 可與任何工具整合
- 支援所有功能

**啟動方式：**
```bash
# 安裝額外依賴
pip install fastapi uvicorn

# 啟動服務
export GEMINI_API_KEY='your-api-key'
python http_api_server.py
```

**API 端點：**
- `POST /chat` - 對話
- `POST /generate-code` - 程式碼生成
- `POST /explain-code` - 程式碼解釋
- `POST /summarize` - 文本摘要
- `GET /tools` - 列出所有工具

## 🚀 實際使用案例

### 案例 1：程式碼審查助手

```bash
# 使用 HTTP API
curl -X POST "http://localhost:8000/tool" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "code_review",
    "arguments": {
      "code": "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"
    }
  }'
```

### 案例 2：VS Code 中的智能重構

1. 選擇一段程式碼
2. 右鍵選擇「Refactor Selected Code」
3. 在新視窗中查看重構建議

### 案例 3：Claude Desktop 中的學習助手

在 Claude 中輸入：
```
請使用 create_study_plan 工具為我制定一個學習 React 的 30 天計劃
```

## 🔧 進階整合

### GitHub Actions 整合

創建 `.github/workflows/code-review.yml`：

```yaml
name: AI Code Review
on: [pull_request]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: AI Code Review
        run: |
          # 使用 HTTP API 進行程式碼審查
          curl -X POST "$API_URL/code-review" \
            -d '{"code": "${{ github.event.pull_request.diff_url }}"}'
```

### Slack 機器人整合

```python
# slack_bot.py
import requests

def gemini_chat(message):
    response = requests.post("http://localhost:8000/chat", 
                           json={"message": message})
    return response.json()["data"]

# 在 Slack 中使用: /gemini 請解釋什麼是 MCP
```

### Raycast 擴展

```typescript
// raycast-extension.tsx
import { ActionPanel, Action, List } from "@raycast/api";

export default function GeminiMCP() {
  return (
    <List>
      <List.Item
        title="Chat with Gemini"
        actions={
          <ActionPanel>
            <Action title="Open Chat" onAction={() => openChat()} />
          </ActionPanel>
        }
      />
    </List>
  );
}
```

## 📊 效能監控

### 監控端點

添加到 HTTP API：

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "uptime": get_uptime(),
        "requests_count": request_counter,
        "gemini_api_status": "connected"
    }
```

### 使用統計

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"{request.method} {request.url} - {duration:.2f}s")
    return response
```

## 🎯 最佳實踐

### 1. 安全性
- 使用環境變數儲存 API 金鑰
- 限制 HTTP API 的訪問來源
- 定期輪換 API 金鑰

### 2. 效能優化
- 實作請求快取
- 使用連接池
- 監控響應時間

### 3. 錯誤處理
- 實作重試機制
- 提供友善的錯誤訊息
- 記錄詳細的錯誤日誌

## 🔮 未來擴展

- **JetBrains IDE 插件**
- **Neovim 插件**
- **Telegram 機器人**
- **Discord 機器人**
- **Alfred Workflow**

選擇最適合你工作流程的整合方式，開始享受 AI 輔助開發的便利！