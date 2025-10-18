"""
Gemini MCP Server - A Model Context Protocol server with Gemini API integration
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .server import GeminiMCPServer
from .gemini_client import GeminiClient

__all__ = ["GeminiMCPServer", "GeminiClient"]