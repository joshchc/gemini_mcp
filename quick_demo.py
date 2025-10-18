#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速使用範例 - Gemini MCP 客戶端
"""

import sys
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 添加當前目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_mcp_client import GeminiMCPClient

def main():
    # 創建客戶端
    client = GeminiMCPClient()
    
    print("🤖 Gemini MCP 快速使用範例")
    print("=" * 40)
    
    try:
        # 1. 檢查狀態
        print("1️⃣ 檢查 API 狀態...")
        status = client.status()
        print(f"   ✅ {status['message']} (版本: {status['version']})")
        
        # 2. 翻譯示例
        print("\n2️⃣ 翻譯功能示例...")
        text_to_translate = "The quick brown fox jumps over the lazy dog"
        translated = client.translate(text_to_translate, "zh-tw")
        print(f"   原文: {text_to_translate}")
        print(f"   翻譯: {translated}")
        
        # 3. 程式碼生成
        print("\n3️⃣ 程式碼生成示例...")
        code_description = "創建一個計算兩數之和的函數"
        generated_code = client.generate_code(code_description, "python")
        print(f"   需求: {code_description}")
        print(f"   生成的程式碼:\n{generated_code[:300]}...")
        
        # 4. 智能問答
        print("\n4️⃣ 智能問答示例...")
        question = "什麼是 API？"
        answer = client.ask_question(question)
        print(f"   問題: {question}")
        print(f"   回答: {answer[:200]}...")
        
        # 5. 情感分析
        print("\n5️⃣ 情感分析示例...")
        text_for_sentiment = "我今天非常開心，因為完成了一個重要的項目！"
        sentiment = client.analyze_sentiment(text_for_sentiment)
        print(f"   文本: {text_for_sentiment}")
        print(f"   情感分析: {sentiment}")
        
        print("\n🎉 所有功能測試完成！")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        print("請確認 API 服務器正在運行在 http://127.0.0.1:8000")

if __name__ == "__main__":
    main()