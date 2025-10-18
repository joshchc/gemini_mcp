"""
Knowledge management plugin for Gemini MCP Server
"""

import logging
from typing import Any, List, Sequence

from mcp.types import Tool, TextContent

from .base import BasePlugin

logger = logging.getLogger(__name__)


class KnowledgeManagementPlugin(BasePlugin):
    """Plugin for knowledge management and Q&A tasks"""
    
    def __init__(self, gemini_client):
        super().__init__(gemini_client)
        self.knowledge_base = {}  # Simple in-memory knowledge base
        
    async def initialize(self):
        """Initialize the knowledge management plugin"""
        logger.info("Knowledge Management Plugin initialized")
        
    async def get_tools(self) -> List[Tool]:
        """Get knowledge management tools"""
        return [
            Tool(
                name="ask_question",
                description="智能問答系統",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "要詢問的問題"
                        },
                        "context": {
                            "type": "string",
                            "description": "相關背景資訊",
                            "default": ""
                        },
                        "domain": {
                            "type": "string",
                            "description": "問題領域 (技術/學術/一般)",
                            "default": "一般"
                        }
                    },
                    "required": ["question"]
                }
            ),
            Tool(
                name="search_knowledge",
                description="搜尋知識庫資訊",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜尋關鍵字或問題"
                        },
                        "category": {
                            "type": "string",
                            "description": "搜尋類別",
                            "default": "全部"
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="organize_information",
                description="整理和分類資訊",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "要整理的內容"
                        },
                        "organization_type": {
                            "type": "string",
                            "description": "整理方式 (分類/摘要/結構化/時間線)",
                            "default": "結構化"
                        }
                    },
                    "required": ["content"]
                }
            ),
            Tool(
                name="create_study_plan",
                description="創建學習計劃",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "學習主題"
                        },
                        "level": {
                            "type": "string",
                            "description": "目標程度 (初級/中級/高級)",
                            "default": "中級"
                        },
                        "duration": {
                            "type": "string",
                            "description": "學習期間",
                            "default": "1個月"
                        }
                    },
                    "required": ["topic"]
                }
            ),
            Tool(
                name="research_topic",
                description="研究特定主題並提供深入分析",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "研究主題"
                        },
                        "depth": {
                            "type": "string",
                            "description": "研究深度 (概述/詳細/專業)",
                            "default": "詳細"
                        },
                        "perspective": {
                            "type": "string",
                            "description": "研究角度",
                            "default": "全面"
                        }
                    },
                    "required": ["topic"]
                }
            ),
            Tool(
                name="compare_concepts",
                description="比較不同概念或理論",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "concept_a": {
                            "type": "string",
                            "description": "第一個概念"
                        },
                        "concept_b": {
                            "type": "string",
                            "description": "第二個概念"
                        },
                        "comparison_aspects": {
                            "type": "string",
                            "description": "比較角度",
                            "default": "全面比較"
                        }
                    },
                    "required": ["concept_a", "concept_b"]
                }
            ),
            Tool(
                name="explain_concept",
                description="解釋複雜概念",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "concept": {
                            "type": "string",
                            "description": "要解釋的概念"
                        },
                        "audience": {
                            "type": "string",
                            "description": "目標受眾 (初學者/中級/專家)",
                            "default": "初學者"
                        },
                        "use_examples": {
                            "type": "boolean",
                            "description": "是否使用例子說明",
                            "default": True
                        }
                    },
                    "required": ["concept"]
                }
            )
        ]
        
    async def can_handle_tool(self, tool_name: str) -> bool:
        """Check if this plugin can handle the tool"""
        return tool_name in [
            "ask_question", "search_knowledge", "organize_information",
            "create_study_plan", "research_topic", "compare_concepts", "explain_concept"
        ]
        
    async def handle_tool_call(self, name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
        """Handle tool calls for knowledge management"""
        try:
            if name == "ask_question":
                question = arguments["question"]
                context = arguments.get("context", "")
                domain = arguments.get("domain", "一般")
                result = await self._ask_question(question, context, domain)
                
            elif name == "search_knowledge":
                query = arguments["query"]
                category = arguments.get("category", "全部")
                result = await self._search_knowledge(query, category)
                
            elif name == "organize_information":
                content = arguments["content"]
                organization_type = arguments.get("organization_type", "結構化")
                result = await self._organize_information(content, organization_type)
                
            elif name == "create_study_plan":
                topic = arguments["topic"]
                level = arguments.get("level", "中級")
                duration = arguments.get("duration", "1個月")
                result = await self._create_study_plan(topic, level, duration)
                
            elif name == "research_topic":
                topic = arguments["topic"]
                depth = arguments.get("depth", "詳細")
                perspective = arguments.get("perspective", "全面")
                result = await self._research_topic(topic, depth, perspective)
                
            elif name == "compare_concepts":
                concept_a = arguments["concept_a"]
                concept_b = arguments["concept_b"]
                comparison_aspects = arguments.get("comparison_aspects", "全面比較")
                result = await self._compare_concepts(concept_a, concept_b, comparison_aspects)
                
            elif name == "explain_concept":
                concept = arguments["concept"]
                audience = arguments.get("audience", "初學者")
                use_examples = arguments.get("use_examples", True)
                result = await self._explain_concept(concept, audience, use_examples)
                
            else:
                raise ValueError(f"Unknown tool: {name}")
                
            return [TextContent(type="text", text=result)]
            
        except Exception as e:
            logger.error(f"Error in knowledge management tool {name}: {e}")
            return [TextContent(
                type="text", 
                text=f"知識管理系統執行時發生錯誤: {str(e)}"
            )]
            
    async def _ask_question(self, question: str, context: str, domain: str) -> str:
        """Answer questions intelligently"""
        context_text = f"\n背景資訊：{context}" if context else ""
        domain_instruction = {
            "技術": "從技術角度深入回答，提供具體實作細節",
            "學術": "提供學術性的嚴謹回答，包含理論依據",
            "一般": "用通俗易懂的語言回答"
        }.get(domain, "用通俗易懂的語言回答")
        
        prompt = f"""
        請{domain_instruction}以下問題：
        
        問題：{question}
        {context_text}
        
        請提供：
        1. 直接回答
        2. 詳細解釋
        3. 相關例子
        4. 進一步學習建議
        
        回答：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _search_knowledge(self, query: str, category: str) -> str:
        """Search knowledge base"""
        prompt = f"""
        請針對查詢「{query}」提供相關知識資訊：
        
        類別範圍：{category}
        
        請提供：
        1. 核心概念說明
        2. 相關知識點
        3. 實際應用
        4. 學習資源推薦
        
        搜尋結果：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _organize_information(self, content: str, organization_type: str) -> str:
        """Organize and structure information"""
        organization_instruction = {
            "分類": "將資訊按主題分類整理",
            "摘要": "提取重點並製作摘要",
            "結構化": "建立清晰的層次結構",
            "時間線": "按時間順序整理"
        }.get(organization_type, "建立清晰的層次結構")
        
        prompt = f"""
        請{organization_instruction}以下內容：
        
        {content}
        
        請提供：
        1. 整理後的結構
        2. 重點摘要
        3. 關鍵資訊標示
        4. 相關性分析
        
        整理結果：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _create_study_plan(self, topic: str, level: str, duration: str) -> str:
        """Create personalized study plan"""
        prompt = f"""
        請為「{topic}」創建一個{level}程度的{duration}學習計劃：
        
        請包含：
        1. 學習目標設定
        2. 階段性里程碑
        3. 詳細學習進度安排
        4. 推薦學習資源
        5. 實作練習建議
        6. 評估檢查點
        
        學習計劃：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _research_topic(self, topic: str, depth: str, perspective: str) -> str:
        """Research topic in depth"""
        depth_instruction = {
            "概述": "提供主題的基本概述",
            "詳細": "深入分析各個面向",
            "專業": "提供專業級的深度分析"
        }.get(depth, "深入分析各個面向")
        
        prompt = f"""
        請從{perspective}角度{depth_instruction}「{topic}」：
        
        請包含：
        1. 主題背景與定義
        2. 核心要素分析
        3. 發展歷史與趨勢
        4. 實際應用案例
        5. 未來發展方向
        6. 相關爭議或挑戰
        
        研究報告：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _compare_concepts(self, concept_a: str, concept_b: str, comparison_aspects: str) -> str:
        """Compare different concepts"""
        prompt = f"""
        請從{comparison_aspects}角度比較「{concept_a}」與「{concept_b}」：
        
        請提供：
        1. 相似性分析
        2. 差異性對比
        3. 各自優缺點
        4. 適用場景
        5. 選擇建議
        6. 整合可能性
        
        比較分析：
        """
        return await self.gemini_client.generate_content(prompt)
        
    async def _explain_concept(self, concept: str, audience: str, use_examples: bool) -> str:
        """Explain complex concepts clearly"""
        audience_instruction = {
            "初學者": "用最簡單的語言，從基礎開始解釋",
            "中級": "提供適度深度的解釋，包含背景知識",
            "專家": "深入技術細節，討論複雜關聯"
        }.get(audience, "用最簡單的語言")
        
        examples_text = "並提供豐富的實例說明" if use_examples else ""
        
        prompt = f"""
        請為{audience}程度的讀者解釋「{concept}」{examples_text}：
        
        請包含：
        1. 概念定義
        2. 核心要素
        3. {"實際例子" if use_examples else "抽象說明"}
        4. 重要性說明
        5. 常見誤解澄清
        6. 延伸學習方向
        
        概念解釋：
        """
        return await self.gemini_client.generate_content(prompt)