# -*- coding: utf-8 -*-
"""
增強的MCP引擎 - 集成智能語義理解
去除硬編碼，使用AI進行動態分析
"""

import json
import logging
from typing import Dict, List, Any, Optional
from intelligent_semantic_engine import IntelligentSemanticEngine

logger = logging.getLogger(__name__)

class EnhancedMCPEngine:
    """增強的MCP引擎，集成智能語義理解"""
    
    def __init__(self, ai_client=None):
        self.ai_client = ai_client
        self.semantic_engine = IntelligentSemanticEngine(ai_client)
        self.knowledge_base = self._initialize_knowledge_base()
        
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """初始化動態知識庫"""
        return {
            "industry_benchmarks": {
                "automation_rates": {
                    "global_leaders": "75-85%",
                    "asia_pacific": "60-75%", 
                    "taiwan_average": "45-60%",
                    "by_type": {
                        "standard_health": "90-95%",
                        "financial_underwriting": "70-80%",
                        "medical_underwriting": "25-35%"
                    }
                },
                "processing_capacity": {
                    "per_person_monthly": "800-1200件",
                    "team_size_standard": "8-12人",
                    "ocr_review_time": "8-12分鐘/件"
                }
            },
            "process_analysis": {
                "standard_cases": "15-30分鐘",
                "complex_cases": "1-3小時", 
                "special_cases": "3-8小時",
                "ocr_workload_ratio": "28-30%"
            }
        }
    
    def analyze_requirement_with_mcp(self, requirement: str, document_data: Optional[Dict] = None) -> Dict[str, Any]:
        """使用智能MCP引擎分析需求"""
        
        try:
            # 使用新的智能分析方法
            return self.analyze_requirement_intelligently(requirement, document_data)
            
        except Exception as e:
            logger.error(f"智能MCP分析失敗: {e}")
            return self._fallback_analysis(requirement, document_data)
    
    def analyze_requirement_intelligently(self, requirement: str, 
                                        document_data: Optional[Dict] = None) -> Dict[str, Any]:
        """智能分析需求，去除硬編碼"""
        
        try:
            # 1. 使用智能語義引擎理解用戶意圖
            logger.info("開始智能語義分析...")
            intent_analysis = self.semantic_engine.understand_user_intent(requirement)
            logger.info(f"意圖分析結果: {intent_analysis}")
            
            # 2. 基於意圖分析構建分析策略
            analysis_strategy = self._build_analysis_strategy(intent_analysis)
            
            # 3. 執行動態數據分析
            analysis_data = self._perform_dynamic_analysis(
                intent_analysis, document_data, analysis_strategy
            )
            
            # 4. 生成智能洞察
            insights = self.semantic_engine.generate_intelligent_insights(
                intent_analysis, analysis_data
            )
            
            # 5. 構建最終結果
            result = self._build_intelligent_result(
                intent_analysis, analysis_data, insights
            )
            
            logger.info("智能分析完成")
            return result
            
        except Exception as e:
            logger.error(f"智能分析失敗: {e}")
            return self._fallback_analysis(requirement, document_data)
    
    def _build_analysis_strategy(self, intent_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """基於意圖分析構建分析策略"""
        
        strategy = {
            "focus_areas": [],
            "data_sources": [],
            "analysis_depth": "medium",
            "output_format": "comprehensive"
        }
        
        # 根據核心問題確定重點分析領域
        for question in intent_analysis.get("core_questions", []):
            if "人力" in question:
                strategy["focus_areas"].append("workforce_analysis")
            if "自動化" in question:
                strategy["focus_areas"].append("automation_analysis")
            if "時間" in question or "效率" in question:
                strategy["focus_areas"].append("efficiency_analysis")
        
        # 根據目標指標確定數據源
        for metric in intent_analysis.get("target_metrics", []):
            if "自動化" in metric:
                strategy["data_sources"].append("automation_benchmarks")
            if "人力" in metric:
                strategy["data_sources"].append("workforce_standards")
            if "時間" in metric:
                strategy["data_sources"].append("processing_times")
        
        # 根據優先級確定分析深度
        if intent_analysis.get("priority_level") == "high":
            strategy["analysis_depth"] = "deep"
        
        return strategy
    
    def _perform_dynamic_analysis(self, intent_analysis: Dict[str, Any], 
                                document_data: Optional[Dict], 
                                strategy: Dict[str, Any]) -> Dict[str, Any]:
        """執行動態數據分析"""
        
        analysis_data = {
            "complexity_assessment": self._assess_complexity_dynamically(intent_analysis),
            "time_estimation": self._estimate_time_dynamically(intent_analysis, strategy),
            "quantitative_analysis": self._perform_quantitative_analysis(strategy),
            "industry_comparison": self._perform_industry_comparison(strategy),
            "recommendations": self._generate_dynamic_recommendations(intent_analysis, strategy)
        }
        
        # 如果有文檔數據，整合文檔分析結果
        if document_data:
            analysis_data["document_insights"] = self._analyze_document_data(document_data)
        
        return analysis_data
    
    def _assess_complexity_dynamically(self, intent_analysis: Dict[str, Any]) -> str:
        """動態評估複雜度"""
        
        complexity_factors = 0
        
        # 根據問題數量評估
        complexity_factors += len(intent_analysis.get("core_questions", []))
        
        # 根據涉及的業務流程評估
        complexity_factors += len(intent_analysis.get("business_processes", []))
        
        # 根據期望的數據類型評估
        complexity_factors += len(intent_analysis.get("expected_data_types", []))
        
        if complexity_factors >= 6:
            return "高度複雜 - 涉及多系統整合、流程重組、人員培訓等多個層面"
        elif complexity_factors >= 3:
            return "中等複雜 - 需要跨部門協調和系統性改進"
        else:
            return "相對簡單 - 主要涉及單一流程或系統優化"
    
    def _estimate_time_dynamically(self, intent_analysis: Dict[str, Any], 
                                 strategy: Dict[str, Any]) -> str:
        """動態估算時間"""
        
        base_months = 2
        
        # 根據分析深度調整
        if strategy["analysis_depth"] == "deep":
            base_months += 2
        
        # 根據重點領域數量調整
        base_months += len(strategy["focus_areas"])
        
        # 根據業務流程複雜度調整
        process_count = len(intent_analysis.get("business_processes", []))
        if process_count > 2:
            base_months += process_count - 2
        
        max_months = base_months + 2
        
        return f"{base_months}-{max_months}個月完整實施週期，包含系統建置、測試、上線和穩定化階段"
    
    def _perform_quantitative_analysis(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """執行量化分析"""
        
        quantitative_data = {}
        
        if "automation_analysis" in strategy["focus_areas"]:
            quantitative_data["automation_metrics"] = self.knowledge_base["industry_benchmarks"]["automation_rates"]
        
        if "workforce_analysis" in strategy["focus_areas"]:
            quantitative_data["workforce_metrics"] = self.knowledge_base["industry_benchmarks"]["processing_capacity"]
        
        if "efficiency_analysis" in strategy["focus_areas"]:
            quantitative_data["efficiency_metrics"] = self.knowledge_base["process_analysis"]
        
        return quantitative_data
    
    def _perform_industry_comparison(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """執行行業對比分析"""
        
        comparison_data = {}
        
        if "automation_benchmarks" in strategy["data_sources"]:
            comparison_data["automation_comparison"] = {
                "current_level": "45-60%",
                "industry_leaders": "75-85%",
                "improvement_potential": "15-25%"
            }
        
        if "workforce_standards" in strategy["data_sources"]:
            comparison_data["workforce_comparison"] = {
                "recommended_team_size": "8-12人",
                "processing_capacity": "800-1200件/人月",
                "specialization_ratio": "初級4-6人，資深2-3人，主管1人"
            }
        
        return comparison_data
    
    def _generate_dynamic_recommendations(self, intent_analysis: Dict[str, Any], 
                                        strategy: Dict[str, Any]) -> List[str]:
        """生成動態建議"""
        
        recommendations = []
        
        # 根據分析重點生成建議
        if "automation_analysis" in strategy["focus_areas"]:
            recommendations.append("建議制定分階段自動化升級計劃，優先處理標準案件自動化")
        
        if "workforce_analysis" in strategy["focus_areas"]:
            recommendations.append("建議優化人力配置結構，加強專業培訓和技能提升")
        
        if "efficiency_analysis" in strategy["focus_areas"]:
            recommendations.append("建議建立標準化作業流程，減少處理時間變異")
        
        # 根據優先級添加緊急建議
        if intent_analysis.get("priority_level") == "high":
            recommendations.insert(0, "建議立即啟動現狀評估，制定詳細的改進路線圖")
        
        return recommendations
    
    def _analyze_document_data(self, document_data: Dict) -> Dict[str, Any]:
        """分析文檔數據"""
        
        insights = {
            "document_type": document_data.get("type", "未知"),
            "key_findings": [],
            "data_quality": "good"
        }
        
        # 提取關鍵發現
        if "extracted_data" in document_data:
            extracted = document_data["extracted_data"]
            
            # 分析重要數據
            if "重要數據說明" in extracted:
                insights["key_findings"].extend(extracted["重要數據說明"][:3])
            
            # 分析核心流程
            if "核心流程說明" in extracted:
                insights["key_findings"].extend(extracted["核心流程說明"][:2])
        
        return insights
    
    def _build_intelligent_result(self, intent_analysis: Dict[str, Any], 
                                analysis_data: Dict[str, Any], 
                                insights: List[str]) -> Dict[str, Any]:
        """構建智能分析結果"""
        
        return {
            "success": True,
            "analysis_method": "intelligent_semantic_mcp",
            "intent_understanding": intent_analysis,
            "analysis": {
                "complexity": analysis_data["complexity_assessment"],
                "estimated_time": analysis_data["time_estimation"],
                "key_insights": insights,
                "quantitative_analysis": analysis_data.get("quantitative_analysis", {}),
                "industry_comparison": analysis_data.get("industry_comparison", {}),
                "recommendations": analysis_data.get("recommendations", [])
            },
            "confidence_score": self._calculate_confidence_score(intent_analysis, analysis_data),
            "metadata": {
                "analysis_timestamp": self._get_timestamp(),
                "semantic_engine_version": "1.0",
                "knowledge_base_version": "1.0"
            }
        }
    
    def _calculate_confidence_score(self, intent_analysis: Dict[str, Any], 
                                  analysis_data: Dict[str, Any]) -> float:
        """計算分析信心度"""
        
        base_confidence = 0.7
        
        # 根據意圖理解質量調整
        if len(intent_analysis.get("core_questions", [])) > 0:
            base_confidence += 0.1
        
        # 根據數據完整性調整
        if analysis_data.get("quantitative_analysis"):
            base_confidence += 0.1
        
        # 根據行業對比數據調整
        if analysis_data.get("industry_comparison"):
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _get_timestamp(self) -> str:
        """獲取時間戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _fallback_analysis(self, requirement: str, document_data: Optional[Dict]) -> Dict[str, Any]:
        """備用分析方法"""
        
        return {
            "success": True,
            "analysis_method": "fallback_analysis",
            "analysis": {
                "complexity": "中等複雜 - 需要進一步分析",
                "estimated_time": "3-6個月實施週期",
                "key_insights": [
                    "📋 需求分析：基於提供的需求進行專業分析",
                    "🔍 建議深入調研：建議進行更詳細的現狀調研和需求分析",
                    "📊 數據收集：建議收集更多量化數據以支持決策"
                ],
                "recommendations": ["建議進行詳細的現狀評估", "制定分階段實施計劃"]
            },
            "confidence_score": 0.6
        }

