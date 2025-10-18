"""
Code assistant plugin for Gemini MCP Server
"""

import logging
from typing import Any, List, Sequence

from mcp.types import Tool, TextContent

from .base import BasePlugin

logger = logging.getLogger(__name__)


class CodeAssistantPlugin(BasePlugin):
    """Plugin for code-related tasks"""
    
    async def initialize(self):
        """Initialize the code assistant plugin"""
        logger.info("Code Assistant Plugin initialized")
        
    async def get_tools(self) -> List[Tool]:
        """Get code assistant tools"""
        return [
            Tool(
                name="generate_code",
                description="根據描述生成程式碼",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": "程式碼功能描述"
                        },
                        "language": {
                            "type": "string",
                            "description": "程式語言",
                            "default": "Python"
                        },
                        "framework": {
                            "type": "string",
                            "description": "使用的框架或函式庫",
                            "default": ""
                        }
                    },
                    "required": ["description"]
                }
            ),
            Tool(
                name="explain_code",
                description="解釋程式碼的功能和邏輯",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "要解釋的程式碼"
                        },
                        "detail_level": {
                            "type": "string",
                            "description": "解釋詳細程度 (簡單/詳細/專家)",
                            "default": "詳細"
                        }
                    },
                    "required": ["code"]
                }
            ),
            Tool(
                name="refactor_code",
                description="程式碼重構建議",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "要重構的程式碼"
                        },
                        "focus": {
                            "type": "string",
                            "description": "重構重點 (效能/可讀性/維護性/全部)",
                            "default": "全部"
                        }
                    },
                    "required": ["code"]
                }
            ),
            Tool(
                name="debug_code",
                description="程式碼錯誤診斷和修復建議",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "有問題的程式碼"
                        },
                        "error_message": {
                            "type": "string",
                            "description": "錯誤訊息",
                            "default": ""
                        },
                        "expected_behavior": {
                            "type": "string",
                            "description": "期望的行為",
                            "default": ""
                        }
                    },
                    "required": ["code"]
                }
            ),
            Tool(
                name="optimize_code",
                description="程式碼效能優化建議",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "要優化的程式碼"
                        },
                        "optimization_type": {
                            "type": "string",
                            "description": "優化類型 (速度/記憶體/可讀性)",
                            "default": "速度"
                        }
                    },
                    "required": ["code"]
                }
            ),
            Tool(
                name="code_review",
                description="程式碼審查和品質評估",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "要審查的程式碼"
                        },
                        "review_criteria": {
                            "type": "string",
                            "description": "審查標準 (安全性/效能/可維護性/全部)",
                            "default": "全部"
                        }
                    },
                    "required": ["code"]
                }
            ),
            Tool(
                name="generate_tests",
                description="生成單元測試",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "要測試的程式碼"
                        },
                        "test_framework": {
                            "type": "string",
                            "description": "測試框架",
                            "default": "pytest"
                        },
                        "coverage_level": {
                            "type": "string",
                            "description": "測試覆蓋程度 (基本/完整/邊界)",
                            "default": "完整"
                        }
                    },
                    "required": ["code"]
                }
            )
        ]
        
    async def can_handle_tool(self, tool_name: str) -> bool:
        """Check if this plugin can handle the tool"""
        return tool_name in [
            "generate_code", "explain_code", "refactor_code", "debug_code",
            "optimize_code", "code_review", "generate_tests"
        ]
        
    async def handle_tool_call(self, name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
        """Handle tool calls for code assistance"""
        try:
            if name == "generate_code":
                description = arguments["description"]
                language = arguments.get("language", "Python")
                framework = arguments.get("framework", "")
                result = await self._generate_code(description, language, framework)
                
            elif name == "explain_code":
                code = arguments["code"]
                detail_level = arguments.get("detail_level", "詳細")
                result = await self._explain_code(code, detail_level)
                
            elif name == "refactor_code":
                code = arguments["code"]
                focus = arguments.get("focus", "全部")
                result = await self._refactor_code(code, focus)
                
            elif name == "debug_code":
                code = arguments["code"]
                error_message = arguments.get("error_message", "")
                expected_behavior = arguments.get("expected_behavior", "")
                result = await self._debug_code(code, error_message, expected_behavior)
                
            elif name == "optimize_code":
                code = arguments["code"]
                optimization_type = arguments.get("optimization_type", "速度")
                result = await self._optimize_code(code, optimization_type)
                
            elif name == "code_review":
                code = arguments["code"]
                review_criteria = arguments.get("review_criteria", "全部")
                result = await self._code_review(code, review_criteria)
                
            elif name == "generate_tests":
                code = arguments["code"]
                test_framework = arguments.get("test_framework", "pytest")
                coverage_level = arguments.get("coverage_level", "完整")
                result = await self._generate_tests(code, test_framework, coverage_level)
                
            else:
                raise ValueError(f"Unknown tool: {name}")
                
            return [TextContent(type="text", text=result)]
            
        except Exception as e:
            logger.error(f"Error in code assistant tool {name}: {e}")
            return [TextContent(
                type="text", 
                text=f"程式碼助手執行時發生錯誤: {str(e)}"
            )]
            
    async def _generate_code(self, description: str, language: str, framework: str) -> str:
        """Generate code based on description"""
        framework_text = f"使用 {framework} 框架" if framework else ""
        prompt = f"""
        請根據以下描述生成 {language} 程式碼{framework_text}：
        
        {description}
        
        請提供：
        1. 完整、可執行的程式碼
        2. 適當的註解說明
        3. 錯誤處理機制
        4. 簡要的使用說明
        
        程式碼：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _explain_code(self, code: str, detail_level: str) -> str:
        """Explain code functionality"""
        level_instruction = {
            "簡單": "用簡單易懂的語言",
            "詳細": "詳細解釋每個部分的功能",
            "專家": "深入分析演算法和設計模式"
        }.get(detail_level, "詳細解釋")
        
        prompt = f"""
        請{level_instruction}解釋以下程式碼：
        
        ```
        {code}
        ```
        
        請包含：
        1. 程式碼的主要功能
        2. 關鍵邏輯說明
        3. 輸入輸出描述
        4. 可能的使用場景
        
        解釋：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _refactor_code(self, code: str, focus: str) -> str:
        """Provide code refactoring suggestions"""
        focus_text = {
            "效能": "重點關注效能優化",
            "可讀性": "重點關注程式碼可讀性",
            "維護性": "重點關注程式碼維護性",
            "全部": "全面分析各個方面"
        }.get(focus, "全面分析")
        
        prompt = f"""
        請分析以下程式碼並提供重構建議，{focus_text}：
        
        ```
        {code}
        ```
        
        請提供：
        1. 問題分析
        2. 重構建議
        3. 改進後的程式碼
        4. 改進說明
        
        重構建議：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _debug_code(self, code: str, error_message: str, expected_behavior: str) -> str:
        """Debug code and provide fix suggestions"""
        error_text = f"\n錯誤訊息：{error_message}" if error_message else ""
        expected_text = f"\n期望行為：{expected_behavior}" if expected_behavior else ""
        
        prompt = f"""
        請幫助診斷以下程式碼的問題：
        
        程式碼：
        ```
        {code}
        ```
        {error_text}
        {expected_text}
        
        請提供：
        1. 問題診斷
        2. 錯誤原因分析
        3. 修復建議
        4. 修正後的程式碼
        5. 預防類似問題的建議
        
        診斷結果：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _optimize_code(self, code: str, optimization_type: str) -> str:
        """Optimize code for performance"""
        prompt = f"""
        請針對{optimization_type}優化以下程式碼：
        
        ```
        {code}
        ```
        
        請提供：
        1. 效能瓶頸分析
        2. 優化策略
        3. 優化後的程式碼
        4. 效能改進說明
        5. 權衡考慮
        
        優化建議：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _code_review(self, code: str, review_criteria: str) -> str:
        """Review code quality"""
        criteria_text = {
            "安全性": "重點檢查安全漏洞",
            "效能": "重點檢查效能問題",
            "可維護性": "重點檢查程式碼可維護性",
            "全部": "全面檢查程式碼品質"
        }.get(review_criteria, "全面檢查")
        
        prompt = f"""
        請對以下程式碼進行審查，{criteria_text}：
        
        ```
        {code}
        ```
        
        請提供：
        1. 程式碼品質評分 (1-10)
        2. 優點分析
        3. 問題點識別
        4. 改進建議
        5. 最佳實踐建議
        
        程式碼審查報告：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _generate_tests(self, code: str, test_framework: str, coverage_level: str) -> str:
        """Generate unit tests for code"""
        coverage_text = {
            "基本": "基本功能測試",
            "完整": "全面的功能和邊界測試",
            "邊界": "重點測試邊界條件和異常情況"
        }.get(coverage_level, "完整")
        
        prompt = f"""
        請為以下程式碼生成 {test_framework} 單元測試，要求{coverage_text}：
        
        ```
        {code}
        ```
        
        請提供：
        1. 完整的測試程式碼
        2. 測試案例說明
        3. 測試數據設計
        4. 執行指令
        
        測試程式碼：
        """
        return await self.gemini_client.generate_content(prompt)