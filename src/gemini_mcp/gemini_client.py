"""
Gemini API client for MCP server
"""

import os
import logging
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

logger = logging.getLogger(__name__)


class GeminiClient:
    """Gemini API client wrapper"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        """
        Initialize Gemini client
        
        Args:
            api_key: Google Gemini API key. If None, will use environment variable
            model_name: Name of the Gemini model to use
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable or api_key parameter is required")
        
        self.model_name = model_name
        self._configure_client()
        self._setup_model()
        
    def _configure_client(self):
        """Configure the Gemini client"""
        genai.configure(api_key=self.api_key)
        
    def _setup_model(self):
        """Setup the Gemini model with safety settings"""
        # Configure safety settings
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
        
        # Generation configuration
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            safety_settings=safety_settings,
            generation_config=generation_config
        )
        
        # Initialize chat for maintaining conversation history
        self.chat = self.model.start_chat(history=[])
        
    async def generate_content(self, prompt: str, use_chat: bool = False) -> str:
        """
        Generate content using Gemini
        
        Args:
            prompt: The input prompt
            use_chat: Whether to use chat mode (maintains conversation history)
            
        Returns:
            Generated text response
        """
        try:
            if use_chat:
                response = await self._send_chat_message(prompt)
            else:
                response = await self._generate_single_response(prompt)
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise
            
    async def _send_chat_message(self, message: str):
        """Send message in chat mode"""
        return self.chat.send_message(message)
        
    async def _generate_single_response(self, prompt: str):
        """Generate single response without chat history"""
        return self.model.generate_content(prompt)
        
    def reset_chat(self):
        """Reset chat history"""
        self.chat = self.model.start_chat(history=[])
        
    def get_chat_history(self) -> List[Dict[str, Any]]:
        """Get current chat history"""
        history = []
        for message in self.chat.history:
            history.append({
                "role": message.role,
                "parts": [part.text for part in message.parts]
            })
        return history
        
    async def summarize_text(self, text: str, max_length: int = 200) -> str:
        """Summarize given text"""
        prompt = f"""
        請用繁體中文總結以下文本，限制在 {max_length} 字以內：
        
        {text}
        
        總結：
        """
        return await self.generate_content(prompt)
        
    async def translate_text(self, text: str, target_language: str = "英文") -> str:
        """Translate text to target language"""
        prompt = f"""
        請將以下文本翻譯成{target_language}：
        
        {text}
        
        翻譯：
        """
        return await self.generate_content(prompt)
        
    async def check_grammar(self, text: str) -> str:
        """Check and correct grammar"""
        prompt = f"""
        請檢查以下文本的語法錯誤並提供修正建議：
        
        {text}
        
        語法檢查結果：
        """
        return await self.generate_content(prompt)
        
    async def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of text"""
        prompt = f"""
        請分析以下文本的情感傾向（正面、負面、中性），並說明原因：
        
        {text}
        
        情感分析：
        """
        return await self.generate_content(prompt)
        
    async def generate_code(self, description: str, language: str = "Python") -> str:
        """Generate code based on description"""
        prompt = f"""
        請根據以下描述生成 {language} 程式碼：
        
        {description}
        
        請提供完整、可執行的程式碼，並加上適當的註解。
        
        程式碼：
        ```{language.lower()}
        """
        response = await self.generate_content(prompt)
        return response + "\n```"
        
    async def explain_code(self, code: str) -> str:
        """Explain given code"""
        prompt = f"""
        請詳細解釋以下程式碼的功能、邏輯和關鍵部分：
        
        ```
        {code}
        ```
        
        程式碼解釋：
        """
        return await self.generate_content(prompt)
        
    async def refactor_code(self, code: str) -> str:
        """Suggest code refactoring"""
        prompt = f"""
        請分析以下程式碼並提供重構建議，包括改進效能、可讀性和維護性的方法：
        
        ```
        {code}
        ```
        
        重構建議：
        """
        return await self.generate_content(prompt)
        
    async def debug_code(self, code: str, error_message: str = "") -> str:
        """Help debug code"""
        prompt = f"""
        請幫助診斷以下程式碼的問題：
        
        程式碼：
        ```
        {code}
        ```
        
        {"錯誤訊息：" + error_message if error_message else ""}
        
        請分析可能的問題並提供解決方案：
        """
        return await self.generate_content(prompt)