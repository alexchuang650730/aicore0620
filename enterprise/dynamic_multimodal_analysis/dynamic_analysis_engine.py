#!/usr/bin/env python3
"""
Dynamic Analysis Engine
動態分析引擎 - 真正智能的需求分析，支持模型容錯和增量優化
"""

import re
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import jieba
import jieba.posseg as pseg

# 設置jieba日誌級別
jieba.setLogLevel(logging.INFO)

@dataclass
class RequirementEntity:
    """需求實體"""
    entity_type: str  # 實體類型：人員、時間、流程、系統等
    value: str       # 實體值
    confidence: float # 置信度
    context: str     # 上下文

@dataclass
class AnalysisContext:
    """分析上下文"""
    domain: str                    # 領域
    entities: List[RequirementEntity]  # 提取的實體
    key_questions: List[str]       # 關鍵問題
    complexity_score: float        # 複雜度分數
    priority_areas: List[str]      # 優先分析領域

class DynamicAnalysisEngine:
    """
    動態分析引擎
    提供真正智能的需求分析，而非硬編碼模板
    """
    
    def __init__(self):
        self.name = "DynamicAnalysisEngine"
        self.logger = logging.getLogger(self.name)
        
        # 使用動態領域知識庫替代硬編碼
        from dynamic_domain_knowledge import dynamic_domain_knowledge
        self.domain_knowledge = dynamic_domain_knowledge
        
        # 模型優先級和容錯配置
        self.model_config = {
            "minimax": {
                "priority": 1,
                "timeout": 30,
                "fallback": "gemini_flash"
            },
            "gemini_flash": {
                "priority": 2, 
                "timeout": 20,
                "fallback": "claude_sonnet"
            },
            "claude_sonnet": {
                "priority": 3,
                "timeout": 25,
                "fallback": "gemini_pro"
            },
            "gemini_pro": {
                "priority": 4,
                "timeout": 30,
                "fallback": "local_analysis"
            }
        }
    
    async def analyze_requirement_dynamic(self, requirement: str, preferred_model: str = "auto") -> Dict[str, Any]:
        """動態分析需求"""
        try:
            # 1. 解析需求內容
            context = self._parse_requirement(requirement)
            
            # 2. 嘗試使用首選模型
            model_result = await self._try_model_analysis(requirement, preferred_model, context)
            
            # 3. 使用增量引擎增強分析
            enhanced_result = await self._enhance_with_incremental_engine(
                requirement, context, model_result
            )
            
            return enhanced_result
            
        except Exception as e:
            self.logger.error(f"動態分析失敗: {e}")
            return self._generate_fallback_analysis(requirement)
    
    def _parse_requirement(self, requirement: str) -> AnalysisContext:
        """解析需求內容"""
        # 1. 檢測領域
        domain = self._detect_domain(requirement)
        
        # 2. 提取實體
        entities = self._extract_entities(requirement, domain)
        
        # 3. 生成關鍵問題
        key_questions = self._generate_key_questions(requirement, domain, entities)
        
        # 4. 計算複雜度
        complexity_score = self._calculate_complexity(requirement, entities)
        
        # 5. 確定優先分析領域
        priority_areas = self._identify_priority_areas(requirement, domain, entities)
        
        return AnalysisContext(
            domain=domain,
            entities=entities,
            key_questions=key_questions,
            complexity_score=complexity_score,
            priority_areas=priority_areas
        )
    
    def _detect_domain(self, requirement: str) -> str:
        """檢測需求領域"""
        return self.domain_knowledge.detect_domain(requirement)
    
    def _extract_entities(self, requirement: str, domain: str) -> List[RequirementEntity]:
        """提取需求實體"""
        entities = []
        
        # 使用jieba進行中文分詞和詞性標註
        words = pseg.cut(requirement)
        
        for word, flag in words:
            entity = self._classify_entity(word, flag, domain)
            if entity:
                entities.append(entity)
        
        # 提取數字和量詞
        number_entities = self._extract_numbers(requirement)
        entities.extend(number_entities)
        
        # 提取時間相關實體
        time_entities = self._extract_time_expressions(requirement)
        entities.extend(time_entities)
        
        return entities
    
    def _classify_entity(self, word: str, pos_tag: str, domain: str) -> Optional[RequirementEntity]:
        """分類實體"""
        # 根據詞性和領域知識分類實體
        if pos_tag in ['n', 'nr', 'ns', 'nt', 'nz']:  # 名詞類
            if domain in self.domain_knowledge:
                domain_config = self.domain_knowledge[domain]
                if word in domain_config["processes"]:
                    return RequirementEntity("process", word, 0.9, "")
                elif word in domain_config["metrics"]:
                    return RequirementEntity("metric", word, 0.8, "")
        
        # 動詞通常表示動作或流程
        elif pos_tag in ['v', 'vn']:
            return RequirementEntity("action", word, 0.7, "")
        
        return None
    
    def _extract_numbers(self, text: str) -> List[RequirementEntity]:
        """提取數字實體"""
        entities = []
        
        # 匹配數字模式
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:人|個人|名|位)',  # 人數
            r'(\d+(?:\.\d+)?)\s*(?:分鐘|小時|天|週|月|年)',  # 時間
            r'(\d+(?:\.\d+)?)\s*(?:%|百分比|比率)',  # 百分比
            r'(\d+(?:\.\d+)?)\s*(?:萬|億|千)',  # 金額
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                value = match.group(1)
                full_match = match.group(0)
                
                if "人" in full_match:
                    entity_type = "人力需求"
                elif any(t in full_match for t in ["分鐘", "小時", "天", "週", "月", "年"]):
                    entity_type = "時間需求"
                elif any(t in full_match for t in ["%", "百分比", "比率"]):
                    entity_type = "比率指標"
                else:
                    entity_type = "數值指標"
                
                entities.append(RequirementEntity(
                    entity_type=entity_type,
                    value=value,
                    confidence=0.9,
                    context=full_match
                ))
        
        return entities
    
    def _extract_time_expressions(self, text: str) -> List[RequirementEntity]:
        """提取時間表達式"""
        entities = []
        
        time_patterns = [
            r'每(?:天|日|週|月|年)',
            r'(?:平均|大概|大約)\s*\d+(?:\.\d+)?\s*(?:分鐘|小時|天)',
            r'(?:需要|花費|耗時)\s*\d+(?:\.\d+)?\s*(?:分鐘|小時|天)'
        ]
        
        for pattern in time_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                entities.append(RequirementEntity(
                    entity_type="時間表達",
                    value=match.group(0),
                    confidence=0.8,
                    context=match.group(0)
                ))
        
        return entities
    
    def _generate_key_questions(self, requirement: str, domain: str, entities: List[RequirementEntity]) -> List[str]:
        """生成關鍵問題"""
        questions = []
        
        # 基於實體生成問題
        has_people = any(e.entity_type == "人力需求" for e in entities)
        has_time = any(e.entity_type == "時間需求" for e in entities)
        has_process = any(e.entity_type == "process" for e in entities)
        
        if not has_people:
            questions.append("需要多少人力資源？")
        
        if not has_time:
            questions.append("預期的時間框架是什麼？")
        
        if not has_process:
            questions.append("具體的業務流程是什麼？")
        
        # 基於領域生成專業問題
        if domain == "insurance":
            if "自動化" in requirement:
                questions.append("現有系統的自動化程度如何？")
            if "OCR" in requirement:
                questions.append("目前OCR系統的準確率是多少？")
        
        return questions
    
    def _calculate_complexity(self, requirement: str, entities: List[RequirementEntity]) -> float:
        """計算需求複雜度"""
        complexity = 0.0
        
        # 基於文本長度
        complexity += min(len(requirement) / 200, 0.3)
        
        # 基於實體數量
        complexity += min(len(entities) / 20, 0.3)
        
        # 基於技術術語
        tech_terms = ["系統", "平台", "API", "數據庫", "算法", "機器學習", "AI"]
        tech_count = sum(1 for term in tech_terms if term in requirement)
        complexity += min(tech_count / 10, 0.2)
        
        # 基於業務複雜度
        business_terms = ["流程", "審核", "合規", "風控", "整合"]
        business_count = sum(1 for term in business_terms if term in requirement)
        complexity += min(business_count / 10, 0.2)
        
        return min(complexity, 1.0)
    
    def _identify_priority_areas(self, requirement: str, domain: str, entities: List[RequirementEntity]) -> List[str]:
        """識別優先分析領域"""
        priority_areas = []
        
        # 基於實體類型確定優先級
        entity_types = [e.entity_type for e in entities]
        
        if "人力需求" in entity_types:
            priority_areas.append("人力資源分析")
        
        if "時間需求" in entity_types:
            priority_areas.append("時間效率分析")
        
        if "比率指標" in entity_types:
            priority_areas.append("績效指標分析")
        
        # 基於關鍵字確定優先級
        if "自動化" in requirement:
            priority_areas.append("自動化潛力評估")
        
        if "成本" in requirement or "費用" in requirement:
            priority_areas.append("成本效益分析")
        
        if "風險" in requirement:
            priority_areas.append("風險評估")
        
        return priority_areas
    
    async def _try_model_analysis(self, requirement: str, preferred_model: str, context: AnalysisContext) -> Dict[str, Any]:
        """嘗試模型分析（支持容錯）"""
        models_to_try = self._get_model_sequence(preferred_model)
        
        for model in models_to_try:
            try:
                self.logger.info(f"嘗試使用模型: {model}")
                result = await self._call_model(model, requirement, context)
                if result and result.get("success", False):
                    result["model_used"] = model
                    return result
                    
            except Exception as e:
                self.logger.warning(f"模型 {model} 分析失敗: {e}")
                continue
        
        # 所有模型都失敗，使用本地分析
        return self._local_analysis(requirement, context)
    
    def _get_model_sequence(self, preferred_model: str) -> List[str]:
        """獲取模型嘗試序列"""
        if preferred_model == "auto":
            return ["minimax", "gemini_flash", "claude_sonnet", "gemini_pro"]
        
        sequence = [preferred_model]
        current = preferred_model
        
        # 根據配置添加後備模型
        while current in self.model_config:
            fallback = self.model_config[current].get("fallback")
            if fallback and fallback not in sequence:
                sequence.append(fallback)
                current = fallback
            else:
                break
        
        return sequence
    
    async def _call_model(self, model: str, requirement: str, context: AnalysisContext) -> Dict[str, Any]:
        """調用特定模型"""
        if model == "minimax":
            return await self._call_minimax(requirement, context)
        elif model == "gemini_flash":
            return await self._call_gemini_flash(requirement, context)
        elif model == "claude_sonnet":
            return await self._call_claude_sonnet(requirement, context)
        elif model == "gemini_pro":
            return await self._call_gemini_pro(requirement, context)
        else:
            return self._local_analysis(requirement, context)
    
    async def _call_minimax(self, requirement: str, context: AnalysisContext) -> Dict[str, Any]:
        """調用MiniMax模型"""
        try:
            # 暫時跳過實際API調用，直接返回本地分析
            self.logger.info("MiniMax API調用跳過，使用本地分析")
            return {"success": False, "error": "MiniMax API暫時不可用"}
            
        except Exception as e:
            self.logger.error(f"MiniMax調用失敗: {e}")
            return {"success": False, "error": str(e)}
    
    def _build_smart_prompt(self, requirement: str, context: AnalysisContext, model: str) -> str:
        """構建智能提示詞"""
        prompt = f"""請分析以下需求並提供專業的結構化回應：

需求描述：{requirement}

分析上下文：
- 領域：{context.domain}
- 複雜度：{context.complexity_score:.2f}
- 關鍵實體：{[f"{e.entity_type}:{e.value}" for e in context.entities[:5]]}
- 優先分析領域：{context.priority_areas}

請基於以上上下文進行深度分析，以JSON格式回應，包含：
{{
    "complexity": "複雜度評估",
    "estimated_time": "預估時間",
    "key_insights": ["關鍵洞察1", "關鍵洞察2"],
    "specific_analysis": {{
        "人力需求": "基於實體分析的具體人力需求",
        "時間分析": "基於實體分析的時間評估",
        "成本效益": "基於領域知識的成本效益分析"
    }},
    "questions": ["需要澄清的問題1", "需要澄清的問題2"],
    "recommendations": ["建議1", "建議2"]
}}

請確保分析結果基於實際輸入內容，而非通用模板。用繁體中文回應。"""
        
        return prompt
    
    def _parse_model_response(self, response_text: str, context: AnalysisContext) -> Dict[str, Any]:
        """解析模型回應"""
        try:
            # 嘗試解析JSON
            parsed = json.loads(response_text)
            return {
                "analysis": parsed,
                "confidence": 0.85,
                "parsing_method": "json"
            }
        except:
            # JSON解析失敗，使用文本解析
            return {
                "analysis": {
                    "complexity": "中等",
                    "estimated_time": "需要進一步分析",
                    "key_insights": [response_text[:200] + "..."],
                    "questions": context.key_questions
                },
                "confidence": 0.6,
                "parsing_method": "text_fallback"
            }
    
    def _local_analysis(self, requirement: str, context: AnalysisContext) -> Dict[str, Any]:
        """本地分析（最後的後備方案）"""
        # 基於解析的上下文生成分析
        analysis = {
            "complexity": self._map_complexity_score(context.complexity_score),
            "estimated_time": self._estimate_time_from_entities(context.entities),
            "key_insights": self._generate_insights_from_entities(context.entities, context.domain),
            "specific_analysis": self._generate_specific_analysis(context),
            "questions": context.key_questions,
            "recommendations": self._generate_recommendations_from_context(context)
        }
        
        return {
            "analysis": analysis,
            "confidence": 0.7,
            "success": True,
            "method": "local_analysis"
        }
    
    def _map_complexity_score(self, score: float) -> str:
        """映射複雜度分數到文字描述"""
        if score < 0.3:
            return "簡單"
        elif score < 0.6:
            return "中等"
        elif score < 0.8:
            return "複雜"
        else:
            return "高度複雜"
    
    def _estimate_time_from_entities(self, entities: List[RequirementEntity]) -> str:
        """基於實體估算時間"""
        time_entities = [e for e in entities if e.entity_type == "時間需求"]
        
        if time_entities:
            # 如果有明確的時間實體，基於此估算
            return f"基於需求分析：{time_entities[0].context}"
        
        # 基於複雜度估算
        people_entities = [e for e in entities if e.entity_type == "人力需求"]
        if people_entities:
            try:
                people_count = float(people_entities[0].value)
                if people_count > 20:
                    return "6-12個月（大型項目）"
                elif people_count > 10:
                    return "3-6個月（中型項目）"
                else:
                    return "1-3個月（小型項目）"
            except:
                pass
        
        return "需要進一步評估"
    
    def _generate_insights_from_entities(self, entities: List[RequirementEntity], domain: str) -> List[str]:
        """基於實體生成洞察"""
        insights = []
        
        # 分析人力需求
        people_entities = [e for e in entities if e.entity_type == "人力需求"]
        if people_entities:
            insights.append(f"識別到人力需求：{people_entities[0].context}")
        
        # 分析時間需求
        time_entities = [e for e in entities if e.entity_type == "時間需求"]
        if time_entities:
            insights.append(f"時間約束：{time_entities[0].context}")
        
        # 分析比率指標
        ratio_entities = [e for e in entities if e.entity_type == "比率指標"]
        if ratio_entities:
            insights.append(f"關鍵指標：{ratio_entities[0].context}")
        
        # 基於領域添加專業洞察
        if domain == "insurance":
            insights.append("保險業務需要重點關注合規性和風險控制")
        
        return insights if insights else ["需要更多信息進行深入分析"]
    
    def _generate_specific_analysis(self, context: AnalysisContext) -> Dict[str, str]:
        """生成具體分析"""
        analysis = {}
        
        # 基於優先領域生成分析
        for area in context.priority_areas:
            if area == "人力資源分析":
                people_entities = [e for e in context.entities if e.entity_type == "人力需求"]
                if people_entities:
                    analysis["人力需求"] = f"基於需求分析，需要{people_entities[0].value}人的團隊"
                else:
                    analysis["人力需求"] = "需要進一步評估具體人力需求"
            
            elif area == "時間效率分析":
                time_entities = [e for e in context.entities if e.entity_type == "時間需求"]
                if time_entities:
                    analysis["時間分析"] = f"時間要求：{time_entities[0].context}"
                else:
                    analysis["時間分析"] = "需要明確時間框架和里程碑"
        
        return analysis
    
    def _generate_recommendations_from_context(self, context: AnalysisContext) -> List[str]:
        """基於上下文生成建議"""
        recommendations = []
        
        if context.complexity_score > 0.7:
            recommendations.append("建議分階段實施，降低項目風險")
        
        if "自動化潛力評估" in context.priority_areas:
            recommendations.append("進行現有流程的自動化可行性評估")
        
        if "成本效益分析" in context.priority_areas:
            recommendations.append("制定詳細的投資回報率計算")
        
        return recommendations if recommendations else ["建議進行更詳細的需求調研"]
    
    async def _enhance_with_incremental_engine(self, requirement: str, context: AnalysisContext, model_result: Dict[str, Any]) -> Dict[str, Any]:
        """使用增量引擎增強分析"""
        try:
            from incremental_engine import IncrementalEngine
            engine = IncrementalEngine()
            
            # 創建基礎版本
            base_data = {
                "requirement": requirement,
                "context": {
                    "domain": context.domain,
                    "entities": [{"type": e.entity_type, "value": e.value} for e in context.entities],
                    "complexity": context.complexity_score
                }
            }
            base_version = engine.create_version(base_data)
            
            # 創建增強版本
            enhanced_data = {**base_data, "model_analysis": model_result}
            enhanced_version = engine.create_version(enhanced_data)
            
            # 進行增量分析
            incremental_analysis = await engine.analyze_incremental_changes(base_version, enhanced_version)
            
            # 整合結果
            final_result = {
                **model_result,
                "incremental_insights": {
                    "analysis_improvements": len(incremental_analysis.changes),
                    "confidence_boost": incremental_analysis.effort_delta,
                    "risk_factors": incremental_analysis.risk_assessment,
                    "enhancement_suggestions": incremental_analysis.recommendations
                },
                "analysis_method": "dynamic_with_incremental_enhancement"
            }
            
            return final_result
            
        except Exception as e:
            self.logger.warning(f"增量引擎增強失敗: {e}")
            # 返回原始模型結果
            model_result["analysis_method"] = "dynamic_without_incremental"
            return model_result
    
    def _generate_fallback_analysis(self, requirement: str) -> Dict[str, Any]:
        """生成後備分析"""
        return {
            "analysis": {
                "complexity": "無法評估",
                "estimated_time": "需要進一步分析",
                "key_insights": ["系統遇到技術問題，請稍後重試"],
                "questions": ["請提供更多詳細信息"],
                "recommendations": ["建議聯繫技術支持"]
            },
            "confidence": 0.1,
            "success": False,
            "error": "所有分析方法都失敗",
            "analysis_method": "emergency_fallback"
        }

    # 其他模型調用方法的占位符
    async def _call_gemini_flash(self, requirement: str, context: AnalysisContext) -> Dict[str, Any]:
        """調用Gemini Flash（實現真實API調用）"""
        try:
            # 這裡可以實現真正的Gemini API調用
            # 暫時返回模擬結果
            logger.info("Gemini Flash API調用（模擬）")
            return {
                "complexity": "中等",
                "estimated_time": "2-4週",
                "key_insights": [
                    "基於Gemini Flash的快速分析",
                    "需要進一步深入研究"
                ],
                "recommendations": [
                    "建議使用更強大的模型進行深度分析"
                ],
                "questions": [
                    "需要更詳細的技術規格嗎？"
                ]
            }
        except Exception as e:
            logger.error(f"Gemini Flash調用異常: {e}")
            return {"success": False, "error": f"Gemini調用異常: {str(e)}"}
    
    async def _call_claude_sonnet(self, requirement: str, context: AnalysisContext) -> Dict[str, Any]:
        """調用Claude Sonnet進行深度分析"""
        try:
            from real_claude_client import call_claude_api
            
            # 構建上下文信息
            claude_context = {
                "domain": context.domain,
                "entities": [entity.value for entity in context.entities],
                "complexity": context.complexity_score,
                "document_content": getattr(context, 'document_content', None)
            }
            
            # 調用真正的Claude API
            result = await call_claude_api(requirement, claude_context)
            
            if result.get("success"):
                logger.info("Claude Sonnet分析成功")
                return result["analysis"]
            else:
                logger.warning(f"Claude Sonnet調用失敗: {result.get('error')}")
                return {"success": False, "error": result.get("error")}
                
        except Exception as e:
            logger.error(f"Claude Sonnet調用異常: {e}")
            return {"success": False, "error": f"Claude調用異常: {str(e)}"}
    
    async def _call_gemini_flash(self, requirement: str, context: AnalysisContext) -> Dict[str, Any]:
        """調用Gemini Flash（實現真實API調用）"""
        try:
            # 這裡可以實現真正的Gemini API調用
            # 暫時返回模擬結果
            logger.info("Gemini Flash API調用（模擬）")
            return {
                "complexity": "中等",
                "estimated_time": "2-4週",
                "key_insights": [
                    "基於Gemini Flash的快速分析",
                    "需要進一步深入研究"
                ],
                "recommendations": [
                    "建議使用更強大的模型進行深度分析"
                ],
                "questions": [
                    "需要更詳細的技術規格嗎？"
                ]
            }
        except Exception as e:
            logger.error(f"Gemini Flash調用異常: {e}")
            return {"success": False, "error": f"Gemini調用異常: {str(e)}"}
    
    async def _call_gemini_pro(self, requirement: str, context: AnalysisContext) -> Dict[str, Any]:
        """調用Gemini Pro（實現真實API調用）"""
        try:
            # 這裡可以實現真正的Gemini Pro API調用
            logger.info("Gemini Pro API調用（模擬）")
            return {
                "complexity": "複雜",
                "estimated_time": "4-8週",
                "key_insights": [
                    "基於Gemini Pro的專業分析",
                    "識別到複雜的業務邏輯",
                    "需要多階段實施"
                ],
                "detailed_analysis": {
                    "business_impact": "高影響業務變革",
                    "technical_requirements": "需要現代化技術棧",
                    "resource_requirements": "需要專業團隊",
                    "risk_assessment": "中等風險，可控制"
                },
                "recommendations": [
                    "建議分階段實施",
                    "建立專業團隊",
                    "制定詳細計劃"
                ],
                "questions": [
                    "現有系統架構如何？",
                    "團隊技術能力如何？"
                ]
            }
        except Exception as e:
            logger.error(f"Gemini Pro調用異常: {e}")
            return {"success": False, "error": f"Gemini調用異常: {str(e)}"}

