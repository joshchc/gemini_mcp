#!/usr/bin/env python3
"""
Simple MCP Server for testing
"""

import asyncio
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from typing import Any, Sequence
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from gemini_mcp.gemini_client import GeminiClient

# Create server instance
server = Server("gemini-mcp")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="chat",
            description="與 Gemini 進行對話",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "要發送的訊息"
                    }
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="generate",
            description="生成文本內容",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "生成內容的提示"
                    }
                },
                "required": ["prompt"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
    """Handle tool calls"""
    # Initialize Gemini client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return [TextContent(type="text", text="錯誤：未設定 GEMINI_API_KEY")]
    
    client = GeminiClient(api_key)
    
    try:
        if name == "chat":
            message = arguments["message"]
            response = await client.generate_content(message, use_chat=True)
            return [TextContent(type="text", text=response)]
            
        elif name == "generate":
            prompt = arguments["prompt"]
            response = await client.generate_content(prompt)
            return [TextContent(type="text", text=response)]
            
        else:
            return [TextContent(type="text", text=f"未知工具: {name}")]
            
    except Exception as e:
        return [TextContent(type="text", text=f"錯誤: {str(e)}")]

async def main():
    """Main entry point"""
    print("🚀 Starting Simple Gemini MCP Server...")
    
    # Initialize with basic options
    from mcp.server.models import InitializationOptions
    from mcp.types import ServerCapabilities
    
    # Create capabilities without calling get_capabilities
    capabilities = ServerCapabilities(
        tools={},
        resources={}
    )
    
    init_options = InitializationOptions(
        server_name="gemini-mcp",
        server_version="1.0.0",
        capabilities=capabilities
    )
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, init_options)

if __name__ == "__main__":
    asyncio.run(main())