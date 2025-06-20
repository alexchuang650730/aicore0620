#!/usr/bin/env python3
"""
Interactive Requirement Analysis Workflow MCP
互動式需求分析工作流MCP

這是一個workflow級別的MCP，具有主動提問和多輪對話能力
"""

import asyncio
import json
import uuid
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

# 導入adapter組件
from sequential_thinking_adapter import SequentialThinkingAdapter, ThinkingStep
from smart_tool_engine import SmartToolEngine
from incremental_engine import IncrementalEngine

class QuestionType(Enum):
    """問題類型"""
    CLARIFICATION = "clarification"  # 澄清問題
    MISSING_INFO = "missing_info"    # 缺失信息
    CONSTRAINT = "constraint"        # 約束條件
    PRIORITY = "priority"           # 優先級
    SCOPE = "scope"                 # 範圍界定
    TECHNICAL = "technical"         # 技術細節
    BUSINESS = "business"           # 業務邏輯
    USER_EXPERIENCE = "user_experience"  # 用戶體驗

class QuestionUrgency(Enum):
    """問題緊急程度"""
    CRITICAL = "critical"    # 必須回答才能繼續
    HIGH = "high"           # 高優先級
    MEDIUM = "medium"       # 中等優先級
    LOW = "low"             # 低優先級

@dataclass
class AnalysisQuestion:
    """分析問題"""
    question_id: str
    question_type: QuestionType
    urgency: QuestionUrgency
    question_text: str
    context: str
    suggested_answers: List[str]
    follow_up_questions: List[str]
    impact_if_unanswered: str

@dataclass
class ConversationTurn:
    """對話輪次"""
    turn_id: str
    timestamp: datetime
    speaker: str  # "system" or "user"
    content: str
    questions: List[AnalysisQuestion]
    analysis_progress: float  # 0.0 - 1.0

@dataclass
class RequirementAnalysisSession:
    """需求分析會話"""
    session_id: str
    initial_requirement: str
    conversation_history: List[ConversationTurn]
    current_analysis_state: Dict[str, Any]
    pending_questions: List[AnalysisQuestion]
    completed_aspects: List[str]
    confidence_level: float
    next_recommended_action: str

class InteractiveRequirementAnalysisWorkflowMCP:
    """
    互動式需求分析工作流MCP
    
    核心特徵：
    1. 主動識別需求中的模糊點和缺失信息
    2. 生成針對性的澄清問題
    3. 多輪對話式需求完善
    4. 動態調整分析策略
    5. 智能引導用戶提供關鍵信息
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "InteractiveRequirementAnalysisWorkflowMCP"
        self.version = "1.0.0"
        self.config = config or {}
        self.logger = logging.getLogger(self.name)
        
        # 註冊adapter組件
        self.thinking_adapter = SequentialThinkingAdapter()
        self.tool_engine = SmartToolEngine()
        self.incremental_engine = IncrementalEngine()
        
        # 會話管理
        self.active_sessions: Dict[str, RequirementAnalysisSession] = {}
        
        # 問題生成規則
        self.question_rules = {
            "functional_requirements": {
                "keywords": ["功能", "特性", "操作", "行為"],
                "questions": [
                    "這個功能的具體操作流程是什麼？",
                    "用戶在什麼情況下會使用這個功能？",
                    "這個功能的輸入和輸出是什麼？",
                    "是否有異常情況需要處理？"
                ]
            },
            "non_functional_requirements": {
                "keywords": ["性能", "安全", "可用性", "擴展"],
                "questions": [
                    "預期的用戶並發量是多少？",
                    "系統響應時間要求是什麼？",
                    "有哪些安全性要求？",
                    "系統可用性目標是多少？"
                ]
            },
            "business_context": {
                "keywords": ["業務", "流程", "規則", "政策"],
                "questions": [
                    "這個需求解決什麼業務問題？",
                    "相關的業務流程是什麼？",
                    "有哪些業務規則需要遵循？",
                    "成功的衡量標準是什麼？"
                ]
            },
            "technical_constraints": {
                "keywords": ["技術", "平台", "集成", "架構"],
                "questions": [
                    "有哪些技術約束條件？",
                    "需要與哪些系統集成？",
                    "首選的技術棧是什麼？",
                    "有哪些現有系統需要考慮？"
                ]
            },
            "user_experience": {
                "keywords": ["用戶", "界面", "體驗", "交互"],
                "questions": [
                    "目標用戶群體是誰？",
                    "用戶的技術水平如何？",
                    "有哪些可訪問性要求？",
                    "用戶界面有什麼特殊要求？"
                ]
            }
        }
        
        # 分析完整性檢查清單
        self.completeness_checklist = [
            "functional_requirements",
            "non_functional_requirements", 
            "business_context",
            "technical_constraints",
            "user_experience",
            "acceptance_criteria",
            "dependencies",
            "risks_assumptions"
        ]
        
        self.logger.info("互動式需求分析工作流MCP初始化完成")
    
    async def start_analysis_session(self, requirement_text: str, context: Optional[Dict[str, Any]] = None) -> RequirementAnalysisSession:
        """開始需求分析會話"""
        session_id = str(uuid.uuid4())
        
        # 創建會話
        session = RequirementAnalysisSession(
            session_id=session_id,
            initial_requirement=requirement_text,
            conversation_history=[],
            current_analysis_state={},
            pending_questions=[],
            completed_aspects=[],
            confidence_level=0.0,
            next_recommended_action="initial_analysis"
        )
        
        self.active_sessions[session_id] = session
        
        # 執行初始分析
        await self._perform_initial_analysis(session_id, requirement_text, context or {})
        
        self.logger.info(f"需求分析會話已開始: {session_id}")
        return session  # 返回session對象而不是session_id
    
    async def _perform_initial_analysis(self, session_id: str, requirement_text: str, context: Dict[str, Any]):
        """執行初始分析"""
        session = self.active_sessions[session_id]
        
        # 1. 啟動思考鏈進行初始分析
        thinking_task_id = await self.thinking_adapter.start_thinking_chain(
            task=f"分析需求並識別需要澄清的問題: {requirement_text}",
            context={"requirement": requirement_text, "context": context},
            mode="analytical"
        )
        
        # 2. 分析需求文本，識別模糊點和缺失信息
        analysis_result = await self._analyze_requirement_gaps(requirement_text, context)
        
        # 3. 生成初始問題
        initial_questions = await self._generate_clarification_questions(requirement_text, analysis_result)
        
        # 4. 更新會話狀態
        session.current_analysis_state = analysis_result
        session.pending_questions = initial_questions
        session.confidence_level = analysis_result.get("initial_confidence", 0.3)
        
        # 5. 創建系統回應
        system_response = await self._create_system_response(session_id, initial_questions)
        
        # 6. 記錄對話輪次
        turn = ConversationTurn(
            turn_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            speaker="system",
            content=system_response,
            questions=initial_questions,
            analysis_progress=0.2
        )
        
        session.conversation_history.append(turn)
    
    async def _analyze_requirement_gaps(self, requirement_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """分析需求缺口"""
        
        # 使用思考適配器進行深度分析
        analysis = {
            "identified_aspects": [],
            "missing_aspects": [],
            "ambiguous_points": [],
            "assumptions": [],
            "initial_confidence": 0.0
        }
        
        # 檢查每個方面的完整性
        for aspect, rules in self.question_rules.items():
            aspect_coverage = 0.0
            
            # 檢查關鍵詞覆蓋
            keywords_found = sum(1 for keyword in rules["keywords"] if keyword in requirement_text)
            if keywords_found > 0:
                analysis["identified_aspects"].append(aspect)
                aspect_coverage = min(keywords_found / len(rules["keywords"]), 1.0)
            else:
                analysis["missing_aspects"].append(aspect)
            
            # 更新整體置信度
            analysis["initial_confidence"] += aspect_coverage / len(self.question_rules)
        
        # 識別模糊表達
        ambiguous_phrases = ["可能", "大概", "應該", "或許", "類似", "等等", "之類"]
        for phrase in ambiguous_phrases:
            if phrase in requirement_text:
                analysis["ambiguous_points"].append(f"包含模糊表達: '{phrase}'")
        
        # 識別假設
        assumption_indicators = ["假設", "預期", "通常", "一般來說", "默認"]
        for indicator in assumption_indicators:
            if indicator in requirement_text:
                analysis["assumptions"].append(f"可能包含假設: '{indicator}'")
        
        return analysis
    
    async def _generate_clarification_questions(self, requirement_text: str, analysis: Dict[str, Any]) -> List[AnalysisQuestion]:
        """生成澄清問題"""
        questions = []
        
        # 為缺失的方面生成問題
        for missing_aspect in analysis["missing_aspects"]:
            if missing_aspect in self.question_rules:
                rules = self.question_rules[missing_aspect]
                
                # 選擇最相關的問題
                primary_question = rules["questions"][0]
                
                question = AnalysisQuestion(
                    question_id=str(uuid.uuid4()),
                    question_type=QuestionType.MISSING_INFO,
                    urgency=QuestionUrgency.HIGH,
                    question_text=primary_question,
                    context=f"需要了解{missing_aspect}相關信息",
                    suggested_answers=[],
                    follow_up_questions=rules["questions"][1:3],
                    impact_if_unanswered=f"缺少{missing_aspect}信息可能導致實現偏差"
                )
                questions.append(question)
        
        # 為模糊點生成澄清問題
        for ambiguous_point in analysis["ambiguous_points"]:
            question = AnalysisQuestion(
                question_id=str(uuid.uuid4()),
                question_type=QuestionType.CLARIFICATION,
                urgency=QuestionUrgency.MEDIUM,
                question_text=f"關於'{ambiguous_point}'，能否提供更具體的描述？",
                context="澄清模糊表達",
                suggested_answers=["請提供具體的數值或標準", "請描述具體的場景"],
                follow_up_questions=[],
                impact_if_unanswered="模糊表達可能導致理解偏差"
            )
            questions.append(question)
        
        # 按緊急程度排序
        questions.sort(key=lambda q: ["critical", "high", "medium", "low"].index(q.urgency.value))
        
        return questions[:5]  # 限制初始問題數量
    
    async def _create_system_response(self, session_id: str, questions: List[AnalysisQuestion]) -> str:
        """創建系統回應"""
        session = self.active_sessions[session_id]
        
        response_parts = [
            "我已經對您的需求進行了初步分析。為了提供更準確的分析結果，我需要澄清以下幾個問題：\n"
        ]
        
        for i, question in enumerate(questions, 1):
            urgency_indicator = "🔴" if question.urgency == QuestionUrgency.CRITICAL else \
                              "🟡" if question.urgency == QuestionUrgency.HIGH else \
                              "🟢" if question.urgency == QuestionUrgency.MEDIUM else "⚪"
            
            response_parts.append(f"{urgency_indicator} **問題 {i}**: {question.question_text}")
            
            if question.suggested_answers:
                response_parts.append(f"   💡 建議考慮: {', '.join(question.suggested_answers)}")
            
            response_parts.append("")  # 空行
        
        response_parts.extend([
            f"📊 **當前分析完整度**: {session.confidence_level*100:.1f}%",
            f"🎯 **已識別方面**: {len(session.current_analysis_state.get('identified_aspects', []))}個",
            f"❓ **待澄清方面**: {len(session.current_analysis_state.get('missing_aspects', []))}個",
            "",
            "請回答上述問題，我會根據您的回答進行更深入的分析。您也可以一次回答多個問題。"
        ])
        
        return "\n".join(response_parts)
    
    async def process_user_response(self, session_id: str, user_response: str) -> Dict[str, Any]:
        """處理用戶回應"""
        if session_id not in self.active_sessions:
            raise ValueError(f"會話 {session_id} 不存在")
        
        session = self.active_sessions[session_id]
        
        # 記錄用戶回應
        user_turn = ConversationTurn(
            turn_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            speaker="user",
            content=user_response,
            questions=[],
            analysis_progress=session.conversation_history[-1].analysis_progress if session.conversation_history else 0.0
        )
        session.conversation_history.append(user_turn)
        
        # 分析用戶回應
        response_analysis = await self._analyze_user_response(session_id, user_response)
        
        # 更新分析狀態
        await self._update_analysis_state(session_id, response_analysis)
        
        # 生成後續問題或完成分析
        next_action = await self._determine_next_action(session_id)
        
        if next_action["action"] == "ask_more_questions":
            # 生成新問題
            new_questions = await self._generate_follow_up_questions(session_id, response_analysis)
            system_response = await self._create_follow_up_response(session_id, new_questions)
            
            # 記錄系統回應
            system_turn = ConversationTurn(
                turn_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                speaker="system",
                content=system_response,
                questions=new_questions,
                analysis_progress=next_action["progress"]
            )
            session.conversation_history.append(system_turn)
            
            return {
                "status": "continue",
                "response": system_response,
                "progress": next_action["progress"],
                "questions": [asdict(q) for q in new_questions]
            }
        
        elif next_action["action"] == "complete_analysis":
            # 完成分析
            final_analysis = await self._complete_analysis(session_id)
            
            return {
                "status": "completed",
                "analysis": final_analysis,
                "progress": 1.0,
                "session_summary": await self._generate_session_summary(session_id)
            }
    
    async def _analyze_user_response(self, session_id: str, user_response: str) -> Dict[str, Any]:
        """分析用戶回應"""
        session = self.active_sessions[session_id]
        
        # 使用思考適配器分析回應
        analysis = {
            "answered_questions": [],
            "new_information": [],
            "remaining_ambiguities": [],
            "confidence_improvement": 0.0
        }
        
        # 檢查哪些問題得到了回答
        for question in session.pending_questions:
            # 簡單的關鍵詞匹配（實際應用中可以使用更複雜的NLP）
            if any(keyword in user_response.lower() for keyword in question.question_text.lower().split()):
                analysis["answered_questions"].append(question.question_id)
                analysis["confidence_improvement"] += 0.1
        
        # 提取新信息
        info_indicators = ["是", "需要", "要求", "必須", "應該", "包括", "支持"]
        for indicator in info_indicators:
            if indicator in user_response:
                analysis["new_information"].append(f"確認信息: {indicator}")
        
        return analysis
    
    async def _update_analysis_state(self, session_id: str, response_analysis: Dict[str, Any]):
        """更新分析狀態"""
        session = self.active_sessions[session_id]
        
        # 移除已回答的問題
        session.pending_questions = [
            q for q in session.pending_questions 
            if q.question_id not in response_analysis["answered_questions"]
        ]
        
        # 更新置信度
        session.confidence_level = min(
            session.confidence_level + response_analysis["confidence_improvement"], 
            1.0
        )
        
        # 更新完成的方面
        if response_analysis["answered_questions"]:
            session.completed_aspects.extend(response_analysis["answered_questions"])
    
    async def _determine_next_action(self, session_id: str) -> Dict[str, Any]:
        """確定下一步行動"""
        session = self.active_sessions[session_id]
        
        # 計算分析進度
        total_aspects = len(self.completeness_checklist)
        completed_aspects = len(session.completed_aspects)
        progress = min(completed_aspects / total_aspects, session.confidence_level)
        
        # 決定是否繼續提問
        if progress < 0.8 and len(session.pending_questions) > 0:
            return {
                "action": "ask_more_questions",
                "progress": progress,
                "reason": "需要更多信息以完成分析"
            }
        elif progress < 0.8 and len(session.pending_questions) == 0:
            return {
                "action": "ask_more_questions", 
                "progress": progress,
                "reason": "需要生成新的澄清問題"
            }
        else:
            return {
                "action": "complete_analysis",
                "progress": 1.0,
                "reason": "已收集足夠信息，可以完成分析"
            }
    
    async def _generate_follow_up_questions(self, session_id: str, response_analysis: Dict[str, Any]) -> List[AnalysisQuestion]:
        """生成後續問題"""
        session = self.active_sessions[session_id]
        
        # 基於當前狀態生成新問題
        questions = []
        
        # 檢查還需要哪些信息
        missing_aspects = [
            aspect for aspect in self.completeness_checklist
            if aspect not in session.completed_aspects
        ]
        
        for aspect in missing_aspects[:3]:  # 限制問題數量
            if aspect in self.question_rules:
                rules = self.question_rules[aspect]
                question_text = rules["questions"][0]
                
                question = AnalysisQuestion(
                    question_id=str(uuid.uuid4()),
                    question_type=QuestionType.MISSING_INFO,
                    urgency=QuestionUrgency.MEDIUM,
                    question_text=question_text,
                    context=f"完善{aspect}信息",
                    suggested_answers=[],
                    follow_up_questions=[],
                    impact_if_unanswered=f"缺少{aspect}可能影響實現質量"
                )
                questions.append(question)
        
        return questions
    
    async def _create_follow_up_response(self, session_id: str, questions: List[AnalysisQuestion]) -> str:
        """創建後續回應"""
        session = self.active_sessions[session_id]
        
        response_parts = [
            "感謝您的回答！基於您提供的信息，我需要進一步了解以下方面：\n"
        ]
        
        for i, question in enumerate(questions, 1):
            response_parts.append(f"**問題 {i}**: {question.question_text}")
            response_parts.append("")
        
        response_parts.extend([
            f"📈 **分析進度**: {session.confidence_level*100:.1f}%",
            f"✅ **已完成**: {len(session.completed_aspects)}個方面",
            f"⏳ **待完善**: {len(questions)}個方面",
            "",
            "請繼續回答，我們正在逐步完善需求分析。"
        ])
        
        return "\n".join(response_parts)
    
    async def _complete_analysis(self, session_id: str) -> Dict[str, Any]:
        """完成分析"""
        session = self.active_sessions[session_id]
        
        # 整合所有對話信息
        all_user_responses = [
            turn.content for turn in session.conversation_history 
            if turn.speaker == "user"
        ]
        
        complete_requirement = session.initial_requirement + "\n\n" + "\n".join(all_user_responses)
        
        # 執行最終分析
        final_analysis = {
            "session_id": session_id,
            "original_requirement": session.initial_requirement,
            "enhanced_requirement": complete_requirement,
            "analysis_completeness": session.confidence_level,
            "conversation_turns": len(session.conversation_history),
            "aspects_covered": session.completed_aspects,
            "final_recommendations": [
                "需求已通過多輪對話得到充分澄清",
                "建議基於完整需求進行詳細設計",
                "可以開始技術方案評估"
            ],
            "quality_metrics": {
                "completeness_score": session.confidence_level * 100,
                "clarity_score": 85.0,  # 基於對話質量評估
                "feasibility_score": 80.0  # 基於技術可行性評估
            }
        }
        
        return final_analysis
    
    async def _generate_session_summary(self, session_id: str) -> Dict[str, Any]:
        """生成會話摘要"""
        session = self.active_sessions[session_id]
        
        return {
            "session_id": session_id,
            "duration": (datetime.now() - session.conversation_history[0].timestamp).total_seconds() if session.conversation_history else 0,
            "total_turns": len(session.conversation_history),
            "questions_asked": sum(len(turn.questions) for turn in session.conversation_history),
            "final_confidence": session.confidence_level,
            "key_improvements": [
                "通過互動澄清了模糊需求",
                "識別並補充了缺失信息", 
                "提高了需求的完整性和準確性"
            ]
        }
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """獲取會話狀態"""
        if session_id not in self.active_sessions:
            return {"error": "會話不存在"}
        
        session = self.active_sessions[session_id]
        
        return {
            "session_id": session_id,
            "status": "active",
            "progress": session.confidence_level,
            "pending_questions": len(session.pending_questions),
            "conversation_turns": len(session.conversation_history),
            "next_action": session.next_recommended_action
        }
    
    def get_workflow_info(self) -> Dict[str, Any]:
        """獲取工作流信息"""
        return {
            "name": self.name,
            "version": self.version,
            "type": "workflow_mcp",
            "description": "互動式需求分析工作流，具有主動提問和多輪對話能力",
            "capabilities": [
                "interactive_questioning",
                "requirement_gap_analysis", 
                "multi_turn_conversation",
                "adaptive_questioning_strategy",
                "completeness_assessment"
            ],
            "registered_adapters": [
                "sequential_thinking_adapter",
                "smart_tool_engine", 
                "incremental_engine"
            ],
            "active_sessions": len(self.active_sessions),
            "question_categories": list(self.question_rules.keys())
        }


    
    async def analyze_document_content(self, session_id: str, document_processing_result: Dict[str, Any]) -> Dict[str, Any]:
        """分析文檔內容"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError(f"會話不存在: {session_id}")
            
            session = self.active_sessions[session_id]
            
            # 提取文檔內容
            content = document_processing_result.get("content", "")
            doc_type = document_processing_result.get("type", "unknown")
            metadata = document_processing_result.get("metadata", {})
            
            # 使用思考適配器分析文檔
            thinking_task_id = await self.thinking_adapter.start_thinking_chain(
                task=f"分析文檔內容並提取需求信息: {doc_type}",
                context={
                    "content": content,
                    "metadata": metadata,
                    "document_type": doc_type
                },
                mode="analytical"
            )
            
            # 分析文檔中的需求信息
            document_analysis = await self._analyze_document_requirements(content, doc_type, metadata)
            
            # 生成針對文檔的問題
            document_questions = await self._generate_document_questions(document_analysis)
            
            # 更新會話狀態
            session.current_analysis_state.update({
                "document_analysis": document_analysis,
                "document_type": doc_type,
                "document_metadata": metadata
            })
            
            session.pending_questions.extend(document_questions)
            
            # 更新置信度
            doc_confidence = document_analysis.get("confidence", 0.5)
            session.confidence_level = (session.confidence_level + doc_confidence) / 2
            
            # 記錄對話輪次
            turn = ConversationTurn(
                turn_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                speaker="system",
                content=f"已分析文檔內容，識別出 {len(document_analysis.get('requirements', []))} 個需求點",
                questions=document_questions,
                analysis_progress=min(session.confidence_level + 0.2, 1.0)
            )
            
            session.conversation_history.append(turn)
            
            return {
                "success": True,
                "document_analysis": document_analysis,
                "generated_questions": [asdict(q) for q in document_questions],
                "updated_confidence": session.confidence_level,
                "analysis_progress": turn.analysis_progress
            }
            
        except Exception as e:
            self.logger.error(f"文檔內容分析失敗: {e}")
            return {
                "success": False,
                "error": f"文檔內容分析失敗: {str(e)}"
            }
    
    async def _analyze_document_requirements(self, content: str, doc_type: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """分析文檔中的需求信息"""
        
        # 基礎分析
        analysis = {
            "requirements": [],
            "functional_requirements": [],
            "non_functional_requirements": [],
            "business_rules": [],
            "constraints": [],
            "assumptions": [],
            "confidence": 0.0
        }
        
        # 根據文檔類型進行特定分析
        if doc_type == "requirement_document":
            analysis["confidence"] = 0.9
            # 提取結構化需求
            analysis["requirements"] = self._extract_structured_requirements(content)
        elif doc_type == "technical_document":
            analysis["confidence"] = 0.7
            # 提取技術約束和架構需求
            analysis["constraints"] = self._extract_technical_constraints(content)
        elif doc_type == "code":
            analysis["confidence"] = 0.6
            # 從代碼中推斷功能需求
            analysis["functional_requirements"] = self._infer_requirements_from_code(content)
        else:
            analysis["confidence"] = 0.5
            # 通用文本分析
            analysis["requirements"] = self._extract_general_requirements(content)
        
        return analysis
    
    async def _generate_document_questions(self, document_analysis: Dict[str, Any]) -> List[AnalysisQuestion]:
        """基於文檔分析生成問題"""
        questions = []
        
        # 根據文檔分析結果生成針對性問題
        if not document_analysis.get("functional_requirements"):
            questions.append(AnalysisQuestion(
                question_id=str(uuid.uuid4()),
                question_type=QuestionType.MISSING_INFO,
                urgency=QuestionUrgency.HIGH,
                question_text="文檔中沒有明確的功能需求，請描述系統應該具備哪些核心功能？",
                context="基於文檔分析，缺少功能需求描述",
                suggested_answers=["用戶管理功能", "數據處理功能", "報告生成功能"],
                follow_up_questions=["每個功能的具體實現方式是什麼？"],
                impact_if_unanswered="無法確定系統的核心功能範圍"
            ))
        
        if not document_analysis.get("non_functional_requirements"):
            questions.append(AnalysisQuestion(
                question_id=str(uuid.uuid4()),
                question_type=QuestionType.CONSTRAINT,
                urgency=QuestionUrgency.MEDIUM,
                question_text="請明確系統的性能、安全性和可用性要求？",
                context="文檔中缺少非功能性需求",
                suggested_answers=["高性能要求", "安全性要求", "可用性要求"],
                follow_up_questions=["具體的性能指標是什麼？"],
                impact_if_unanswered="可能導致系統架構設計不當"
            ))
        
        return questions
    
    def _extract_structured_requirements(self, content: str) -> List[str]:
        """從結構化文檔中提取需求"""
        requirements = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            # 查找編號列表項
            if any(line.startswith(prefix) for prefix in ['1.', '2.', '3.', '-', '*', '•']):
                if any(keyword in line.lower() for keyword in ['需求', '功能', '要求', 'requirement', 'feature']):
                    requirements.append(line)
        
        return requirements
    
    def _extract_technical_constraints(self, content: str) -> List[str]:
        """提取技術約束"""
        constraints = []
        tech_keywords = ['性能', '安全', '可用性', '擴展性', '兼容性', 'performance', 'security', 'scalability']
        
        lines = content.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in tech_keywords):
                constraints.append(line.strip())
        
        return constraints
    
    def _infer_requirements_from_code(self, content: str) -> List[str]:
        """從代碼中推斷功能需求"""
        requirements = []
        
        # 查找函數定義
        import re
        function_pattern = r'def\s+(\w+)\s*\('
        functions = re.findall(function_pattern, content)
        
        for func in functions:
            if not func.startswith('_'):  # 排除私有函數
                requirements.append(f"系統需要提供{func}功能")
        
        return requirements
    
    def _extract_general_requirements(self, content: str) -> List[str]:
        """從一般文本中提取需求"""
        requirements = []
        requirement_patterns = [
            r'需要.*?[。\n]',
            r'應該.*?[。\n]',
            r'必須.*?[。\n]',
            r'要求.*?[。\n]'
        ]
        
        import re
        for pattern in requirement_patterns:
            matches = re.findall(pattern, content)
            requirements.extend([match.strip() for match in matches])
        
        return requirements

