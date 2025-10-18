"""
Base plugin class for Gemini MCP plugins
"""

from abc import ABC, abstractmethod
from typing import Any, List, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.types import Tool, Resource, TextContent, ImageContent, EmbeddedResource


class BasePlugin(ABC):
    """Base class for all MCP plugins"""
    
    def __init__(self, gemini_client):
        self.gemini_client = gemini_client
        
    @abstractmethod
    async def initialize(self):
        """Initialize the plugin"""
        pass
        
    @abstractmethod
    async def get_tools(self) -> List[Any]:  # Tool
        """Get tools provided by this plugin"""
        pass
        
    @abstractmethod
    async def can_handle_tool(self, tool_name: str) -> bool:
        """Check if this plugin can handle the given tool"""
        pass
        
    @abstractmethod
    async def handle_tool_call(self, name: str, arguments: dict[str, Any]) -> Sequence[Any]:  # TextContent | ImageContent | EmbeddedResource
        """Handle tool call for this plugin"""
        pass
        
    async def get_resources(self) -> List[Any]:  # Resource
        """Get resources provided by this plugin (optional)"""
        return []