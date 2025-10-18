"""
Text processing plugin for Gemini MCP Server
"""

import logging
from typing import Any, List, Sequence

from mcp.types import Tool, TextContent

from .base import BasePlugin

logger = logging.getLogger(__name__)


class TextProcessingPlugin(BasePlugin):
    """Plugin for text processing tasks"""
    
    async def initialize(self):
        """Initialize the text processing plugin"""
        logger.info("Text Processing Plugin initialized")
        
    async def get_tools(self) -> List[Tool]:
        """Get text processing tools"""
        return [
            Tool(
                name="summarize",
                description="摘要文本內容",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "要摘要的文本"
                        },
                        "max_length": {
                            "type": "integer",
                            "description": "摘要最大字數",
                            "default": 200
                        }
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="translate",
                description="翻譯文本到指定語言",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "要翻譯的文本"
                        },
                        "target_language": {
                            "type": "string",
                            "description": "目標語言",
                            "default": "英文"
                        }
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="check_grammar",
                description="檢查文本語法並提供修正建議",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "要檢查的文本"
                        }
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="analyze_sentiment",
                description="分析文本情感傾向",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "要分析的文本"
                        }
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="extract_keywords",
                description="提取文本關鍵詞",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "要提取關鍵詞的文本"
                        },
                        "count": {
                            "type": "integer",
                            "description": "要提取的關鍵詞數量",
                            "default": 10
                        }
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="rewrite_text",
                description="重寫文本以改善表達",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "要重寫的文本"
                        },
                        "style": {
                            "type": "string",
                            "description": "重寫風格 (正式/非正式/學術/商業)",
                            "default": "正式"
                        }
                    },
                    "required": ["text"]
                }
            )
        ]
        
    async def can_handle_tool(self, tool_name: str) -> bool:
        """Check if this plugin can handle the tool"""
        return tool_name in [
            "summarize", "translate", "check_grammar", 
            "analyze_sentiment", "extract_keywords", "rewrite_text"
        ]
        
    async def handle_tool_call(self, name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
        """Handle tool calls for text processing"""
        try:
            if name == "summarize":
                text = arguments["text"]
                max_length = arguments.get("max_length", 200)
                result = await self.gemini_client.summarize_text(text, max_length)
                
            elif name == "translate":
                text = arguments["text"]
                target_language = arguments.get("target_language", "英文")
                result = await self.gemini_client.translate_text(text, target_language)
                
            elif name == "check_grammar":
                text = arguments["text"]
                result = await self.gemini_client.check_grammar(text)
                
            elif name == "analyze_sentiment":
                text = arguments["text"]
                result = await self.gemini_client.analyze_sentiment(text)
                
            elif name == "extract_keywords":
                text = arguments["text"]
                count = arguments.get("count", 10)
                result = await self._extract_keywords(text, count)
                
            elif name == "rewrite_text":
                text = arguments["text"]
                style = arguments.get("style", "正式")
                result = await self._rewrite_text(text, style)
                
            else:
                raise ValueError(f"Unknown tool: {name}")
                
            return [TextContent(type="text", text=result)]
            
        except Exception as e:
            logger.error(f"Error in text processing tool {name}: {e}")
            return [TextContent(
                type="text", 
                text=f"文本處理時發生錯誤: {str(e)}"
            )]
            
    async def _extract_keywords(self, text: str, count: int) -> str:
        """Extract keywords from text"""
        prompt = f"""
        請從以下文本中提取 {count} 個最重要的關鍵詞，按重要性排序：
        
        {text}
        
        請以清單形式列出關鍵詞，每行一個：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _rewrite_text(self, text: str, style: str) -> str:
        """Rewrite text in specified style"""
        prompt = f"""
        請將以下文本重寫為{style}的風格，保持原意但改善表達：
        
        {text}
        
        重寫後的文本：
        """
        return await self.gemini_client.generate_content(prompt)