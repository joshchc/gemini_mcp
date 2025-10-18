#!/usr/bin/env python3
"""
Test MCP Server functionality
"""

import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gemini_mcp.gemini_client import GeminiClient

async def test_mcp_functionality():
    """Test core MCP functionality"""
    print("🧪 Testing MCP Server Components")
    print("================================")
    
    # Test Gemini client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not set")
        return False
    
    try:
        print("📡 Testing Gemini client...")
        client = GeminiClient(api_key)
        
        # Test basic generation
        response = await client.generate_content("請說 '你好，MCP 測試成功！'")
        print(f"✅ Response: {response[:100]}...")
        
        # Test tools functionality
        print("\n🔧 Testing tool functions...")
        
        # Test summarization
        summary = await client.summarize_text("這是一個很長的測試文本，需要被摘要。它包含了很多重要的資訊。", 50)
        print(f"✅ Summarization: {summary[:100]}...")
        
        # Test code generation  
        code = await client.generate_code("建立一個函數來計算兩個數字的和", "Python")
        print(f"✅ Code generation: {code[:100]}...")
        
        print("\n🎉 All MCP functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_mcp_tools():
    """Test MCP tools structure"""
    print("\n🛠️ Testing MCP Tools Structure")
    print("==============================")
    
    # Import plugins
    try:
        from gemini_mcp.plugins.text_processing import TextProcessingPlugin
        from gemini_mcp.plugins.code_assistant import CodeAssistantPlugin
        from gemini_mcp.plugins.knowledge_management import KnowledgeManagementPlugin
        
        api_key = os.getenv("GEMINI_API_KEY")
        client = GeminiClient(api_key)
        
        # Test text processing plugin
        text_plugin = TextProcessingPlugin(client)
        await text_plugin.initialize()
        tools = await text_plugin.get_tools()
        print(f"✅ Text Processing Plugin: {len(tools)} tools")
        
        # Test code assistant plugin
        code_plugin = CodeAssistantPlugin(client)
        await code_plugin.initialize()
        tools = await code_plugin.get_tools()
        print(f"✅ Code Assistant Plugin: {len(tools)} tools")
        
        # Test knowledge management plugin
        knowledge_plugin = KnowledgeManagementPlugin(client)
        await knowledge_plugin.initialize()
        tools = await knowledge_plugin.get_tools()
        print(f"✅ Knowledge Management Plugin: {len(tools)} tools")
        
        print("\n🎉 All plugin tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Plugin test error: {e}")
        return False

async def main():
    """Main test runner"""
    print("🚀 Gemini MCP Server Test Suite")
    print("================================\n")
    
    results = []
    
    # Test core functionality
    results.append(await test_mcp_functionality())
    
    # Test plugin structure
    results.append(await test_mcp_tools())
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! MCP server components are working correctly.")
        print("\n📝 MCP Server is ready to use!")
        print("   - Use 'python simple_server.py' to start the server")
        print("   - Configure your MCP client to connect to this server")
        print("   - Available tools: chat, generate, and 20+ plugin tools")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())