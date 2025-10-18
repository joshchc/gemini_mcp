#!/usr/bin/env python3
"""
HTTP API Server for Gemini MCP
"""

import asyncio
import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()
from typing import Dict, Any, Optional
import uvicorn

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gemini_mcp.gemini_client import GeminiClient
from gemini_mcp.plugins.text_processing import TextProcessingPlugin
from gemini_mcp.plugins.code_assistant import CodeAssistantPlugin
from gemini_mcp.plugins.knowledge_management import KnowledgeManagementPlugin

app = FastAPI(
    title="Gemini MCP HTTP API",
    description="HTTP API for Gemini MCP Server",
    version="1.0.0"
)

# Global variables
client = None
plugins = {}

class ChatRequest(BaseModel):
    message: str
    use_history: bool = True

class GenerateRequest(BaseModel):
    prompt: str

class ToolRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

class APIResponse(BaseModel):
    success: bool
    data: Optional[str] = None
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize Gemini client and plugins"""
    global client, plugins
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is required")
    
    # Initialize client
    client = GeminiClient(api_key)
    
    # Initialize plugins
    plugins = {
        "text_processing": TextProcessingPlugin(client),
        "code_assistant": CodeAssistantPlugin(client),
        "knowledge_management": KnowledgeManagementPlugin(client)
    }
    
    # Initialize all plugins
    for plugin in plugins.values():
        await plugin.initialize()
    
    print("🚀 Gemini MCP HTTP API started successfully!")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Gemini MCP HTTP API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/tools")
async def list_tools():
    """List all available tools"""
    tools = []
    
    # Core tools
    tools.extend([
        {"name": "chat", "description": "與 Gemini 進行對話"},
        {"name": "generate", "description": "生成文本內容"},
        {"name": "reset_chat", "description": "重置對話歷史"}
    ])
    
    # Plugin tools
    for plugin in plugins.values():
        plugin_tools = await plugin.get_tools()
        for tool in plugin_tools:
            tools.append({
                "name": tool.name,
                "description": tool.description
            })
    
    return {"tools": tools}

@app.post("/chat", response_model=APIResponse)
async def chat(request: ChatRequest):
    """Chat with Gemini"""
    try:
        response = await client.generate_content(
            request.message, 
            use_chat=request.use_history
        )
        return APIResponse(success=True, data=response)
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/generate", response_model=APIResponse)
async def generate(request: GenerateRequest):
    """Generate content"""
    try:
        response = await client.generate_content(request.prompt)
        return APIResponse(success=True, data=response)
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/reset-chat", response_model=APIResponse)
async def reset_chat():
    """Reset chat history"""
    try:
        client.reset_chat()
        return APIResponse(success=True, data="對話歷史已重置")
    except Exception as e:
        return APIResponse(success=False, error=str(e))

@app.post("/tool", response_model=APIResponse)
async def call_tool(request: ToolRequest):
    """Call a specific tool"""
    try:
        tool_name = request.tool_name
        arguments = request.arguments
        
        # Check if any plugin can handle this tool
        for plugin in plugins.values():
            if await plugin.can_handle_tool(tool_name):
                result = await plugin.handle_tool_call(tool_name, arguments)
                # Extract text from TextContent objects
                text_result = ""
                for item in result:
                    if hasattr(item, 'text'):
                        text_result += item.text
                    else:
                        text_result += str(item)
                return APIResponse(success=True, data=text_result)
        
        return APIResponse(success=False, error=f"Unknown tool: {tool_name}")
        
    except Exception as e:
        return APIResponse(success=False, error=str(e))

# Convenient endpoints for common operations
@app.post("/summarize")
async def summarize(text: str, max_length: int = 200):
    """Summarize text"""
    return await call_tool(ToolRequest(
        tool_name="summarize",
        arguments={"text": text, "max_length": max_length}
    ))

@app.post("/translate")
async def translate(text: str, target_language: str = "英文"):
    """Translate text"""
    return await call_tool(ToolRequest(
        tool_name="translate",
        arguments={"text": text, "target_language": target_language}
    ))

@app.post("/generate-code")
async def generate_code(description: str, language: str = "Python"):
    """Generate code"""
    return await call_tool(ToolRequest(
        tool_name="generate_code",
        arguments={"description": description, "language": language}
    ))

@app.post("/explain-code")
async def explain_code(code: str):
    """Explain code"""
    return await call_tool(ToolRequest(
        tool_name="explain_code",
        arguments={"code": code}
    ))

if __name__ == "__main__":
    # Check API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Please set GEMINI_API_KEY environment variable")
        sys.exit(1)
    
    print("🚀 Starting Gemini MCP HTTP API Server...")
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000,
        log_level="info"
    )