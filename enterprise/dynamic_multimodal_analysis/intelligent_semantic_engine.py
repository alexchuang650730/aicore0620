# -*- coding: utf-8 -*-
"""
智能語義理解引擎
去除硬編碼，使用AI進行動態問題理解和回答生成
"""

import re
import json
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class IntelligentSemanticEngine:
    """智能語義理解引擎"""
    
    def __init__(self, ai_client=None):
        self.ai_client = ai_client
        self.domain_knowledge = self._load_domain_knowledge()
        
    def _load_domain_knowledge(self) -> Dict[str, Any]:
        """加載領域知識庫"""
        return {
            "insurance_metrics": [
                "自動化比率", "處理時間", "人力配置", "準確率", 
                "處理量", "成本效益", "投資回報", "風險評估"
            ],
            "process_types": [
                "核保流程", "理賠流程", "承保流程", "出單流程",
                "收文流程", "審核流程", "建檔流程"
            ],
            "measurement_units": [
                "人月", "工時", "件數", "比率", "金額", "時間"
            ]
        }
    
    def understand_user_intent(self, user_requirement: str) -> Dict[str, Any]:
        """使用AI理解用戶真正的問題意圖"""
        
        if not self.ai_client:
            # 如果沒有AI客戶端，使用基礎語義分析
            return self._basic_semantic_analysis(user_requirement)
        
        try:
            # 構建智能分析提示
            analysis_prompt = self._build_intent_analysis_prompt(user_requirement)
            
            # 調用AI進行語義理解
            ai_response = self.ai_client.generate_response(analysis_prompt)
            
            # 解析AI回應
            intent_analysis = self._parse_intent_response(ai_response)
            
            logger.info(f"AI語義理解結果: {intent_analysis}")
            return intent_analysis
            
        except Exception as e:
            logger.warning(f"AI語義理解失敗，使用基礎分析: {e}")
            return self._basic_semantic_analysis(user_requirement)
    
    def _build_intent_analysis_prompt(self, user_requirement: str) -> str:
        """構建意圖分析提示"""
        return f"""
請分析以下用戶需求，提取核心問題和期望的信息類型：

用戶需求: "{user_requirement}"

請從以下角度分析：
1. 用戶想了解的具體指標或數據
2. 用戶關心的業務流程或環節  
3. 用戶期望的量化信息類型
4. 問題的優先級和重要程度

請以JSON格式返回分析結果：
{{
    "core_questions": ["問題1", "問題2", ...],
    "target_metrics": ["指標1", "指標2", ...],
    "business_processes": ["流程1", "流程2", ...],
    "expected_data_types": ["數據類型1", "數據類型2", ...],
    "priority_level": "high/medium/low",
    "answer_strategy": "如何組織回答的策略"
}}
"""
    
    def _parse_intent_response(self, ai_response: str) -> Dict[str, Any]:
        """解析AI的意圖分析回應"""
        try:
            # 嘗試提取JSON部分
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # 如果沒有JSON，進行文本解析
                return self._parse_text_response(ai_response)
        except Exception as e:
            logger.warning(f"解析AI回應失敗: {e}")
            return self._basic_semantic_analysis(ai_response)
    
    def _basic_semantic_analysis(self, text: str) -> Dict[str, Any]:
        """基礎語義分析（無AI時的備用方案）"""
        
        # 動態提取關鍵概念
        metrics = self._extract_metrics_concepts(text)
        processes = self._extract_process_concepts(text)
        data_types = self._extract_data_type_concepts(text)
        
        # 分析問題類型
        question_types = self._analyze_question_types(text)
        
        return {
            "core_questions": question_types,
            "target_metrics": metrics,
            "business_processes": processes,
            "expected_data_types": data_types,
            "priority_level": self._assess_priority(text),
            "answer_strategy": self._determine_answer_strategy(question_types, metrics)
        }
    
    def _extract_metrics_concepts(self, text: str) -> List[str]:
        """動態提取指標概念"""
        found_metrics = []
        
        # 使用語義相似度而不是硬編碼匹配
        for metric in self.domain_knowledge["insurance_metrics"]:
            if self._semantic_similarity(text, metric) > 0.3:
                found_metrics.append(metric)
        
        # 提取數字相關的概念
        number_contexts = re.findall(r'(\w+[^。，,.\n]*\d+[%\w]*[^。，,.\n]*)', text)
        for context in number_contexts:
            metric_type = self._classify_metric_from_context(context)
            if metric_type and metric_type not in found_metrics:
                found_metrics.append(metric_type)
        
        return found_metrics
    
    def _extract_process_concepts(self, text: str) -> List[str]:
        """動態提取流程概念"""
        found_processes = []
        
        # 識別流程相關詞彙
        process_indicators = ['流程', '程序', '作業', 'SOP', '標準', '步驟']
        
        for indicator in process_indicators:
            if indicator in text:
                # 提取該指示詞周圍的上下文
                contexts = self._extract_context_around_word(text, indicator, window=10)
                for context in contexts:
                    process_type = self._classify_process_from_context(context)
                    if process_type and process_type not in found_processes:
                        found_processes.append(process_type)
        
        return found_processes
    
    def _extract_data_type_concepts(self, text: str) -> List[str]:
        """動態提取數據類型概念"""
        data_types = []
        
        # 識別量化詞彙
        if re.search(r'多少|幾個|數量|比率|百分比', text):
            data_types.append("數量統計")
        
        if re.search(r'時間|期間|週期|月|年', text):
            data_types.append("時間分析")
        
        if re.search(r'人|員工|人力|團隊', text):
            data_types.append("人力資源")
        
        if re.search(r'成本|費用|投資|效益', text):
            data_types.append("成本效益")
        
        return data_types
    
    def _semantic_similarity(self, text1: str, text2: str) -> float:
        """計算語義相似度（簡化版本）"""
        # 這裡可以使用更複雜的語義相似度算法
        # 目前使用簡單的詞彙重疊度
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _classify_metric_from_context(self, context: str) -> Optional[str]:
        """從上下文分類指標類型"""
        context_lower = context.lower()
        
        if any(word in context_lower for word in ['自動', '自動化', '機器']):
            return "自動化指標"
        elif any(word in context_lower for word in ['準確', '精確', '正確']):
            return "準確性指標"
        elif any(word in context_lower for word in ['時間', '速度', '效率']):
            return "效率指標"
        elif any(word in context_lower for word in ['人', '員工', '人力']):
            return "人力指標"
        elif any(word in context_lower for word in ['成本', '費用', '投資']):
            return "成本指標"
        
        return None
    
    def _classify_process_from_context(self, context: str) -> Optional[str]:
        """從上下文分類流程類型"""
        context_lower = context.lower()
        
        if any(word in context_lower for word in ['核保', '審核', '評估']):
            return "核保流程"
        elif any(word in context_lower for word in ['收文', '進件', '接收']):
            return "收文流程"
        elif any(word in context_lower for word in ['出單', '建檔', '發行']):
            return "出單流程"
        elif any(word in context_lower for word in ['理賠', '賠付', '給付']):
            return "理賠流程"
        
        return None
    
    def _extract_context_around_word(self, text: str, word: str, window: int = 5) -> List[str]:
        """提取詞彙周圍的上下文"""
        contexts = []
        words = text.split()
        
        for i, w in enumerate(words):
            if word in w:
                start = max(0, i - window)
                end = min(len(words), i + window + 1)
                context = ' '.join(words[start:end])
                contexts.append(context)
        
        return contexts
    
    def _analyze_question_types(self, text: str) -> List[str]:
        """分析問題類型"""
        questions = []
        
        # 識別疑問詞和問題模式
        if re.search(r'多少|幾個|什麼|如何|怎麼', text):
            if re.search(r'多少.*人|幾個.*人|人力|人員', text):
                questions.append("人力需求分析")
            
            if re.search(r'比率|百分比|自動化', text):
                questions.append("自動化程度分析")
            
            if re.search(r'時間|期間|週期', text):
                questions.append("時間效率分析")
            
            if re.search(r'流程|程序|步驟', text):
                questions.append("流程分析")
        
        return questions if questions else ["綜合業務分析"]
    
    def _assess_priority(self, text: str) -> str:
        """評估問題優先級"""
        high_priority_indicators = ['急', '重要', '關鍵', '核心', '主要']
        medium_priority_indicators = ['一般', '普通', '常規']
        
        if any(indicator in text for indicator in high_priority_indicators):
            return "high"
        elif any(indicator in text for indicator in medium_priority_indicators):
            return "medium"
        else:
            return "medium"  # 默認中等優先級
    
    def _determine_answer_strategy(self, question_types: List[str], metrics: List[str]) -> str:
        """確定回答策略"""
        if "人力需求分析" in question_types:
            return "優先提供人力配置和工作量分析"
        elif "自動化程度分析" in question_types:
            return "重點分析自動化現狀和行業對比"
        elif len(metrics) > 3:
            return "提供全面的量化分析報告"
        else:
            return "提供針對性的專業分析"

    def generate_intelligent_insights(self, intent_analysis: Dict[str, Any], 
                                    analysis_data: Dict[str, Any]) -> List[str]:
        """基於意圖分析生成智能洞察"""
        
        if not self.ai_client:
            return self._generate_rule_based_insights(intent_analysis, analysis_data)
        
        try:
            # 構建洞察生成提示
            insight_prompt = self._build_insight_generation_prompt(intent_analysis, analysis_data)
            
            # 調用AI生成洞察
            ai_response = self.ai_client.generate_response(insight_prompt)
            
            # 解析生成的洞察
            insights = self._parse_insights_response(ai_response)
            
            return insights
            
        except Exception as e:
            logger.warning(f"AI洞察生成失敗，使用規則生成: {e}")
            return self._generate_rule_based_insights(intent_analysis, analysis_data)
    
    def _build_insight_generation_prompt(self, intent_analysis: Dict[str, Any], 
                                       analysis_data: Dict[str, Any]) -> str:
        """構建洞察生成提示"""
        return f"""
基於以下用戶意圖分析和數據，生成專業的業務洞察：

用戶意圖分析：
{json.dumps(intent_analysis, ensure_ascii=False, indent=2)}

分析數據：
{json.dumps(analysis_data, ensure_ascii=False, indent=2)}

請生成3-5個專業洞察，要求：
1. 直接回答用戶的核心問題
2. 提供具體的量化數據
3. 包含行業對比和建議
4. 使用專業但易懂的語言

請以列表格式返回洞察，每個洞察一行。
"""
    
    def _parse_insights_response(self, ai_response: str) -> List[str]:
        """解析AI生成的洞察回應"""
        insights = []
        
        # 按行分割並清理
        lines = ai_response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 10:
                # 移除列表標記
                line = re.sub(r'^\d+\.\s*', '', line)
                line = re.sub(r'^[-*]\s*', '', line)
                insights.append(line)
        
        return insights[:5]  # 最多返回5個洞察
    
    def _generate_rule_based_insights(self, intent_analysis: Dict[str, Any], 
                                    analysis_data: Dict[str, Any]) -> List[str]:
        """基於規則生成洞察（AI不可用時的備用方案）"""
        insights = []
        
        # 根據問題類型生成相應洞察
        for question_type in intent_analysis.get("core_questions", []):
            if "人力需求" in question_type:
                insights.append("👥 人力配置分析：根據業務量和流程複雜度，建議配置專業團隊以確保處理效率")
            
            elif "自動化程度" in question_type:
                insights.append("🤖 自動化現狀：當前自動化水平與行業領先者存在差距，有較大提升空間")
            
            elif "時間效率" in question_type:
                insights.append("⏱️ 效率分析：處理時間因案件複雜度而異，標準化流程可顯著提升效率")
        
        # 根據指標類型添加洞察
        for metric in intent_analysis.get("target_metrics", []):
            if "自動化" in metric:
                insights.append("📊 自動化建議：通過技術升級和流程優化，可實現更高的自動化比率")
        
        return insights[:3] if insights else ["📋 綜合分析：基於現有數據提供專業的業務分析和改進建議"]

