"""
Plugin system for Gemini MCP Server
"""

from .text_processing import TextProcessingPlugin
from .code_assistant import CodeAssistantPlugin  
from .knowledge_management import KnowledgeManagementPlugin

__all__ = [
    "TextProcessingPlugin",
    "CodeAssistantPlugin", 
    "KnowledgeManagementPlugin"
]