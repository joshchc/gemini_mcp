"""
Simple test script for Gemini MCP Server
"""

import asyncio
import os
import sys
import logging

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from gemini_mcp.gemini_client import GeminiClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_gemini_client():
    """Test basic Gemini client functionality"""
    logger.info("Testing Gemini client...")
    
    # Set up API key for testing
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable is required for testing")
        return False
    
    try:
        # Initialize client
        client = GeminiClient(api_key)
        logger.info("✓ Gemini client initialized")
        
        # Test basic generation
        response = await client.generate_content("說 '你好，這是測試訊息'")
        logger.info(f"✓ Basic generation test: {response[:100]}...")
        
        # Test chat mode
        chat_response = await client.generate_content("我的名字是測試員", use_chat=True)
        logger.info(f"✓ Chat mode test: {chat_response[:100]}...")
        
        # Test follow-up in chat
        followup = await client.generate_content("我剛才說我的名字是什麼？", use_chat=True)
        logger.info(f"✓ Chat follow-up test: {followup[:100]}...")
        
        # Test summarization
        text_to_summarize = """
        人工智慧（AI）是電腦科學的一個分支，致力於創建能夠執行通常需要人類智慧的任務的機器。
        這包括學習、推理、問題解決、感知和語言理解。AI系統可以分為狹義AI和通用AI。
        狹義AI專門設計來執行特定任務，而通用AI則具有人類水準的認知能力。
        機器學習是AI的一個子集，使電腦能夠從數據中學習而無需明確編程。
        """
        summary = await client.summarize_text(text_to_summarize, 50)
        logger.info(f"✓ Summarization test: {summary[:100]}...")
        
        # Test translation
        translation = await client.translate_text("Hello, how are you?", "繁體中文")
        logger.info(f"✓ Translation test: {translation[:100]}...")
        
        logger.info("All tests passed! ✅")
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False


async def test_code_generation():
    """Test code generation functionality"""
    logger.info("Testing code generation...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return False
        
    try:
        client = GeminiClient(api_key)
        
        # Test code generation
        code = await client.generate_code("創建一個計算費波納契數列的函數", "Python")
        logger.info(f"✓ Code generation test: {code[:200]}...")
        
        # Test code explanation
        simple_code = """
        def fibonacci(n):
            if n <= 1:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
        """
        explanation = await client.explain_code(simple_code)
        logger.info(f"✓ Code explanation test: {explanation[:200]}...")
        
        logger.info("Code generation tests passed! ✅")
        return True
        
    except Exception as e:
        logger.error(f"Code generation test failed: {e}")
        return False


async def main():
    """Run all tests"""
    logger.info("Starting Gemini MCP Server tests...")
    
    tests = [
        test_gemini_client,
        test_code_generation
    ]
    
    results = []
    for test in tests:
        result = await test()
        results.append(result)
        
    passed = sum(results)
    total = len(results)
    
    logger.info(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        logger.info("🎉 All tests passed!")
        return 0
    else:
        logger.error("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())