#!/usr/bin/env python3
"""
Simple test script for Gemini integration
"""

import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gemini_mcp.gemini_client import GeminiClient


async def demo():
    """Demo the Gemini MCP functionality"""
    print("🚀 Gemini MCP Server Demo")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Please set GEMINI_API_KEY environment variable")
        print("   export GEMINI_API_KEY='your-api-key'")
        return
    
    try:
        # Initialize client
        print("🔧 Initializing Gemini client...")
        client = GeminiClient(api_key)
        print("✅ Client initialized successfully!")
        
        # Test basic conversation
        print("\n💬 Testing basic conversation...")
        response = await client.generate_content("請用繁體中文介紹一下 Model Context Protocol (MCP)")
        print(f"Response: {response[:500]}...")
        
        # Test text processing
        print("\n📝 Testing text summarization...")
        long_text = """
        Model Context Protocol (MCP) 是一個開放標準，用於連接大型語言模型 (LLM) 和外部數據源及工具。
        MCP 允許 LLM 安全地訪問本地和遠程資源，包括文件系統、數據庫、API 和其他服務。
        通過 MCP，開發者可以創建能夠與真實世界數據交互的 AI 應用，而不僅僅是依賴訓練數據。
        這個協議設計為可擴展、安全且易於實現，支持各種客戶端和服務器實現。
        MCP 的核心概念包括資源 (Resources)、工具 (Tools) 和提示 (Prompts)，
        這些組件共同工作來提供豐富的上下文給 LLM。
        """
        summary = await client.summarize_text(long_text, 100)
        print(f"Summary: {summary}")
        
        # Test code generation
        print("\n💻 Testing code generation...")
        code = await client.generate_code("創建一個計算質數的 Python 函數", "Python")
        print(f"Generated code:\n{code[:300]}...")
        
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(demo())