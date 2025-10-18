"""
Configuration settings for Gemini MCP Server
"""

import os
from typing import Optional


class Config:
    """Configuration class for the MCP server"""
    
    def __init__(self):
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.max_tokens: int = int(os.getenv("MAX_TOKENS", "8192"))
        self.temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
        
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        return True


# Global config instance
config = Config()


def get_config() -> Config:
    """Get configuration instance"""
    return config