"""
Gemini MCP Client - Python 客戶端庫
方便在 Python 代碼中直接使用 MCP 工具
"""

import requests
import json
from typing import Dict, Any, Optional

class GeminiMCPClient:
    """Gemini MCP HTTP API 客戶端"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        """
        初始化客戶端
        
        Args:
            base_url: API 服務器地址
        """
        self.base_url = base_url.rstrip('/')
        
    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """發送 POST 請求"""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()
    
    def _get(self, endpoint: str) -> Dict[str, Any]:
        """發送 GET 請求"""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def status(self) -> Dict[str, Any]:
        """檢查 API 狀態"""
        return self._get("/")
    
    def get_tools(self) -> Dict[str, Any]:
        """獲取可用工具列表"""
        return self._get("/tools")
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        調用工具
        
        Args:
            tool_name: 工具名稱
            arguments: 工具參數
            
        Returns:
            工具執行結果
        """
        response = self._post("/tool", {
            "tool_name": tool_name,
            "arguments": arguments
        })
        
        if response.get("success"):
            return response["data"]
        else:
            raise Exception(f"工具調用失敗: {response.get('error')}")
    
    def generate(self, prompt: str) -> str:
        """生成文本內容"""
        response = self._post("/generate", {"prompt": prompt})
        if response.get("success"):
            return response["data"]
        else:
            raise Exception(f"生成失敗: {response.get('error')}")
    
    def chat(self, message: str, use_history: bool = True) -> str:
        """與 Gemini 聊天"""
        response = self._post("/chat", {
            "message": message,
            "use_history": use_history
        })
        if response.get("success"):
            return response["data"]
        else:
            raise Exception(f"聊天失敗: {response.get('error')}")
    
    def translate(self, text: str, target_language: str = "zh-tw") -> str:
        """翻譯文本"""
        return self.call_tool("translate", {
            "text": text,
            "target_language": target_language
        })
    
    def summarize(self, text: str, max_length: Optional[int] = None) -> str:
        """文本摘要"""
        args = {"text": text}
        if max_length:
            args["max_length"] = max_length
        return self.call_tool("summarize", args)
    
    def generate_code(self, description: str, language: str = "python") -> str:
        """生成程式碼"""
        return self.call_tool("generate_code", {
            "description": description,
            "language": language
        })
    
    def explain_code(self, code: str, language: str = "python") -> str:
        """解釋程式碼"""
        return self.call_tool("explain_code", {
            "code": code,
            "language": language
        })
    
    def code_review(self, code: str, language: str = "python") -> str:
        """程式碼審查"""
        return self.call_tool("code_review", {
            "code": code,
            "language": language
        })
    
    def debug_code(self, code: str, error_message: str, language: str = "python") -> str:
        """程式碼除錯"""
        return self.call_tool("debug_code", {
            "code": code,
            "error_message": error_message,
            "language": language
        })
    
    def check_grammar(self, text: str) -> str:
        """語法檢查"""
        return self.call_tool("check_grammar", {"text": text})
    
    def analyze_sentiment(self, text: str) -> str:
        """情感分析"""
        return self.call_tool("analyze_sentiment", {"text": text})
    
    def ask_question(self, question: str, context: Optional[str] = None) -> str:
        """智能問答"""
        args = {"question": question}
        if context:
            args["context"] = context
        return self.call_tool("ask_question", args)

# 使用範例
if __name__ == "__main__":
    # 創建客戶端
    client = GeminiMCPClient()
    
    try:
        # 檢查狀態
        status = client.status()
        print(f"✅ API 狀態: {status}")
        
        # 翻譯示例
        translation = client.translate("Hello, World!", "zh-tw")
        print(f"🔄 翻譯結果: {translation}")
        
        # 生成程式碼示例
        code = client.generate_code("創建一個計算階乘的函數", "python")
        print(f"💻 生成的程式碼:\n{code[:200]}...")
        
        # 智能問答示例
        answer = client.ask_question("什麼是機器學習？")
        print(f"🤖 問答結果: {answer[:200]}...")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")