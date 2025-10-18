#!/usr/bin/env python3
"""
Gemini MCP Server startup script
"""

import asyncio
import os
import sys

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from gemini_mcp.server import main

if __name__ == "__main__":
    asyncio.run(main())