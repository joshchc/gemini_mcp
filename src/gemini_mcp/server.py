"""
Main MCP server with Gemini integration
"""

import asyncio
import logging
import os
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
)

from .gemini_client import GeminiClient
from .plugins.text_processing import TextProcessingPlugin
from .plugins.code_assistant import CodeAssistantPlugin
from .plugins.knowledge_management import KnowledgeManagementPlugin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiMCPServer:
    """Main MCP server class with Gemini integration"""
    
    def __init__(self):
        self.server = Server("gemini-mcp")
        self.gemini_client = None
        self.plugins = {}
        
    async def initialize(self):
        """Initialize the server and plugins"""
        try:
            # Initialize Gemini client
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable is required")
                
            self.gemini_client = GeminiClient(api_key)
            
            # Initialize plugins
            await self._initialize_plugins()
            
            # Register handlers
            self._register_handlers()
            
            logger.info("Gemini MCP Server initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize server: {e}")
            raise
            
    async def _initialize_plugins(self):
        """Initialize all plugins"""
        self.plugins = {
            "text_processing": TextProcessingPlugin(self.gemini_client),
            "code_assistant": CodeAssistantPlugin(self.gemini_client),
            "knowledge_management": KnowledgeManagementPlugin(self.gemini_client)
        }
        
        for name, plugin in self.plugins.items():
            await plugin.initialize()
            logger.info(f"Initialized plugin: {name}")
            
    def _register_handlers(self):
        """Register MCP handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List available tools"""
            tools = []
            
            # Core conversation tools
            tools.extend([
                Tool(
                    name="chat",
                    description="與 Gemini 進行對話，支援多輪對話",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "要發送的訊息"
                            },
                            "use_history": {
                                "type": "boolean",
                                "description": "是否使用對話歷史",
                                "default": True
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
                ),
                Tool(
                    name="reset_chat",
                    description="重置對話歷史",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ])
            
            # Add plugin tools
            for plugin in self.plugins.values():
                tools.extend(await plugin.get_tools())
                
            return tools
            
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
            """Handle tool calls"""
            try:
                # Core tools
                if name == "chat":
                    message = arguments["message"]
                    use_history = arguments.get("use_history", True)
                    
                    response = await self.gemini_client.generate_content(
                        message, 
                        use_chat=use_history
                    )
                    
                    return [TextContent(type="text", text=response)]
                    
                elif name == "generate":
                    prompt = arguments["prompt"]
                    response = await self.gemini_client.generate_content(prompt)
                    return [TextContent(type="text", text=response)]
                    
                elif name == "reset_chat":
                    self.gemini_client.reset_chat()
                    return [TextContent(type="text", text="對話歷史已重置")]
                
                # Plugin tools
                for plugin in self.plugins.values():
                    if await plugin.can_handle_tool(name):
                        return await plugin.handle_tool_call(name, arguments)
                        
                raise ValueError(f"Unknown tool: {name}")
                
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(
                    type="text", 
                    text=f"執行工具時發生錯誤: {str(e)}"
                )]
                
        @self.server.list_resources()
        async def handle_list_resources() -> list[dict]:
            """List available resources"""
            return []
            
    async def run(self):
        """Run the server"""
        await self.initialize()
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream)


async def main():
    """Main entry point"""
    server = GeminiMCPServer()
    try:
        await server.run()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())