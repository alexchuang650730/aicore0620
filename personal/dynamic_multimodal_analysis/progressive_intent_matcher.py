#!/usr/bin/env python3
"""
三層漸進式智能意圖匹配引擎
架構：搜尋引擎 → 六大工作流 → KiloCode 兜底

第一層：Cloud Search MCP (入口層)
第二層：Six Workflow MCPs (處理層)  
第三層：KiloCode MCP (兜底層)

作者: PowerAutomation 團隊
版本: 1.0.0
日期: 2025-06-18
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("progressive_intent_matcher")

class ProcessingLayer(Enum):
    """處理層級枚舉"""
    SEARCH_ENGINE = "search_engine"      # 第一層：搜尋引擎
    WORKFLOW_MCPS = "workflow_mcps"      # 第二層：六大工作流
    KILOCODE_FALLBACK = "kilocode_fallback"  # 第三層：KiloCode 兜底

class WorkflowType(Enum):
    """六大工作流類型"""
    REQUIREMENTS_ANALYSIS = "requirements_analysis"
    ARCHITECTURE_DESIGN = "architecture_design"
    CODING_IMPLEMENTATION = "coding_implementation"
    TESTING_VALIDATION = "testing_validation"
    DEPLOYMENT_OPERATIONS = "deployment_operations"
    MAINTENANCE_SUPPORT = "maintenance_support"

@dataclass
class IntentAnalysisResult:
    """意圖分析結果"""
    confidence: float
    recommended_layer: ProcessingLayer
    workflow_type: Optional[WorkflowType]
    reasoning: str
    search_keywords: List[str]
    complexity_score: float

class ProgressiveIntentMatcher:
    """三層漸進式智能意圖匹配引擎"""
    
    def __init__(self):
        self.name = "ProgressiveIntentMatcher"
        
        # MCP 工具註冊表
        self.mcp_tools = {
            # 第一層：搜尋引擎
            "cloud_search_mcp": {
                "layer": ProcessingLayer.SEARCH_ENGINE,
                "capabilities": ["semantic_search", "knowledge_retrieval", "intent_analysis"],
                "confidence_threshold": 0.7,
                "status": "available"
            },
            
            # 第二層：六大工作流 MCP
            "requirements_analysis_mcp": {
                "layer": ProcessingLayer.WORKFLOW_MCPS,
                "workflow_type": WorkflowType.REQUIREMENTS_ANALYSIS,
                "capabilities": ["requirement_gathering", "stakeholder_analysis", "user_story_creation"],
                "confidence_threshold": 0.8,
                "status": "available"
            },
            "architecture_design_mcp": {
                "layer": ProcessingLayer.WORKFLOW_MCPS,
                "workflow_type": WorkflowType.ARCHITECTURE_DESIGN,
                "capabilities": ["system_design", "component_architecture", "technology_selection"],
                "confidence_threshold": 0.8,
                "status": "available"
            },
            "coding_implementation_mcp": {
                "layer": ProcessingLayer.WORKFLOW_MCPS,
                "workflow_type": WorkflowType.CODING_IMPLEMENTATION,
                "capabilities": ["code_generation", "algorithm_implementation", "framework_integration"],
                "confidence_threshold": 0.8,
                "status": "available"
            },
            "testing_validation_mcp": {
                "layer": ProcessingLayer.WORKFLOW_MCPS,
                "workflow_type": WorkflowType.TESTING_VALIDATION,
                "capabilities": ["test_design", "quality_assurance", "performance_testing"],
                "confidence_threshold": 0.8,
                "status": "available"
            },
            "deployment_operations_mcp": {
                "layer": ProcessingLayer.WORKFLOW_MCPS,
                "workflow_type": WorkflowType.DEPLOYMENT_OPERATIONS,
                "capabilities": ["deployment_automation", "infrastructure_management", "monitoring_setup"],
                "confidence_threshold": 0.8,
                "status": "available"
            },
            "maintenance_support_mcp": {
                "layer": ProcessingLayer.WORKFLOW_MCPS,
                "workflow_type": WorkflowType.MAINTENANCE_SUPPORT,
                "capabilities": ["bug_fixing", "performance_optimization", "feature_enhancement"],
                "confidence_threshold": 0.8,
                "status": "available"
            },
            
            # 第三層：KiloCode 兜底
            "kilocode_mcp": {
                "layer": ProcessingLayer.KILOCODE_FALLBACK,
                "capabilities": ["tool_creation", "custom_solution", "unlimited_problem_solving"],
                "confidence_threshold": 0.0,  # 兜底層，總是可用
                "status": "available"
            }
        }
        
        # 輔助工具
        self.auxiliary_tools = {
            "sequential_thinking_mcp": ["task_decomposition", "reflection_engine", "dependency_analysis"],
            "rl_srt_mcp": ["reinforcement_learning", "self_reinforcing_training", "adaptive_optimization"],
            "cloud_edge_data_mcp": ["data_processing", "model_training", "performance_monitoring"],
            "local_model_mcp": ["local_inference", "offline_processing", "privacy_protection"],
            "enhanced_smartui_mcp": ["ui_generation", "dynamic_adaptation", "user_experience"]
        }
        
        # 處理統計
        self.processing_stats = {
            "total_requests": 0,
            "layer_usage": {layer.value: 0 for layer in ProcessingLayer},
            "workflow_usage": {workflow.value: 0 for workflow in WorkflowType},
            "success_rate": 0.0,
            "average_processing_time": 0.0
        }
        
        logger.info("三層漸進式智能意圖匹配引擎初始化完成")
    
    async def analyze_user_intent(self, user_input: str, context: Dict[str, Any] = None) -> IntentAnalysisResult:
        """分析用戶意圖，決定處理層級"""
        
        logger.info(f"開始分析用戶意圖: {user_input}")
        
        # 使用 Cloud Search MCP 進行初步分析
        search_result = await self._call_cloud_search_analysis(user_input, context)
        
        # 基於搜尋結果決定處理策略
        if search_result["can_be_resolved_by_search"]:
            # 第一層：搜尋引擎可以解決
            return IntentAnalysisResult(
                confidence=search_result["confidence"],
                recommended_layer=ProcessingLayer.SEARCH_ENGINE,
                workflow_type=None,
                reasoning="問題可以通過搜尋和知識檢索解決",
                search_keywords=search_result["keywords"],
                complexity_score=search_result["complexity"]
            )
        
        elif search_result["requires_workflow_processing"]:
            # 第二層：需要工作流處理
            workflow_type = self._determine_workflow_type(search_result)
            return IntentAnalysisResult(
                confidence=search_result["confidence"],
                recommended_layer=ProcessingLayer.WORKFLOW_MCPS,
                workflow_type=workflow_type,
                reasoning=f"需要 {workflow_type.value} 工作流處理",
                search_keywords=search_result["keywords"],
                complexity_score=search_result["complexity"]
            )
        
        else:
            # 第三層：KiloCode 兜底
            return IntentAnalysisResult(
                confidence=1.0,  # 兜底層總是有信心
                recommended_layer=ProcessingLayer.KILOCODE_FALLBACK,
                workflow_type=None,
                reasoning="需要創建新工具或自定義解決方案",
                search_keywords=search_result["keywords"],
                complexity_score=search_result["complexity"]
            )
    
    async def process_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """處理用戶請求的主要方法"""
        
        start_time = datetime.now()
        self.processing_stats["total_requests"] += 1
        
        try:
            # 第一步：分析用戶意圖
            intent_result = await self.analyze_user_intent(user_input, context)
            
            # 第二步：根據推薦層級進行處理
            if intent_result.recommended_layer == ProcessingLayer.SEARCH_ENGINE:
                result = await self._process_with_search_engine(user_input, intent_result, context)
                
            elif intent_result.recommended_layer == ProcessingLayer.WORKFLOW_MCPS:
                result = await self._process_with_workflow_mcps(user_input, intent_result, context)
                
            else:  # KILOCODE_FALLBACK
                result = await self._process_with_kilocode_fallback(user_input, intent_result, context)
            
            # 更新統計信息
            self.processing_stats["layer_usage"][intent_result.recommended_layer.value] += 1
            if intent_result.workflow_type:
                self.processing_stats["workflow_usage"][intent_result.workflow_type.value] += 1
            
            # 計算處理時間
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "status": "success",
                "result": result,
                "processing_info": {
                    "layer_used": intent_result.recommended_layer.value,
                    "workflow_type": intent_result.workflow_type.value if intent_result.workflow_type else None,
                    "confidence": intent_result.confidence,
                    "reasoning": intent_result.reasoning,
                    "processing_time": processing_time
                }
            }
            
        except Exception as e:
            logger.error(f"處理請求失敗: {str(e)}")
            return {
                "status": "error",
                "message": f"處理失敗: {str(e)}",
                "fallback_suggestion": "建議使用 KiloCode 兜底處理"
            }
    
    async def _call_cloud_search_analysis(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """調用 Cloud Search MCP 進行意圖分析"""
        
        # 模擬 Cloud Search MCP 調用
        logger.info("調用 Cloud Search MCP 進行意圖分析")
        
        # 這裡應該是實際的 MCP 調用
        # 目前返回模擬結果
        
        # 簡單的關鍵詞分析來決定處理策略
        keywords = user_input.lower().split()
        
        # 判斷是否可以通過搜尋解決
        search_indicators = ["什麼是", "如何", "為什麼", "介紹", "說明", "解釋"]
        can_search_resolve = any(indicator in user_input for indicator in search_indicators)
        
        # 判斷是否需要工作流處理
        workflow_indicators = ["開發", "建立", "創建", "設計", "實現", "部署", "測試"]
        needs_workflow = any(indicator in user_input for indicator in workflow_indicators)
        
        # 計算複雜度
        complexity = len(keywords) / 10.0  # 簡單的複雜度計算
        
        return {
            "can_be_resolved_by_search": can_search_resolve and not needs_workflow,
            "requires_workflow_processing": needs_workflow,
            "confidence": 0.8 if can_search_resolve or needs_workflow else 0.6,
            "keywords": keywords,
            "complexity": min(complexity, 1.0),
            "analysis_details": {
                "search_indicators_found": [ind for ind in search_indicators if ind in user_input],
                "workflow_indicators_found": [ind for ind in workflow_indicators if ind in user_input]
            }
        }
    
    def _determine_workflow_type(self, search_result: Dict[str, Any]) -> WorkflowType:
        """根據搜尋結果決定工作流類型"""
        
        keywords = " ".join(search_result["keywords"])
        
        # 工作流關鍵詞映射
        workflow_keywords = {
            WorkflowType.REQUIREMENTS_ANALYSIS: ["需求", "分析", "用戶故事", "功能"],
            WorkflowType.ARCHITECTURE_DESIGN: ["架構", "設計", "系統", "組件"],
            WorkflowType.CODING_IMPLEMENTATION: ["開發", "編碼", "實現", "程式", "代碼"],
            WorkflowType.TESTING_VALIDATION: ["測試", "驗證", "品質", "檢查"],
            WorkflowType.DEPLOYMENT_OPERATIONS: ["部署", "發布", "運維", "監控"],
            WorkflowType.MAINTENANCE_SUPPORT: ["維護", "修復", "優化", "支援"]
        }
        
        # 計算每個工作流的匹配分數
        scores = {}
        for workflow_type, workflow_keys in workflow_keywords.items():
            score = sum(1 for key in workflow_keys if key in keywords)
            scores[workflow_type] = score
        
        # 返回分數最高的工作流類型
        best_workflow = max(scores, key=scores.get)
        
        # 如果沒有明確匹配，默認使用編碼工作流
        if scores[best_workflow] == 0:
            return WorkflowType.CODING_IMPLEMENTATION
        
        return best_workflow
    
    async def _process_with_search_engine(self, user_input: str, intent_result: IntentAnalysisResult, context: Dict[str, Any]) -> Dict[str, Any]:
        """使用搜尋引擎處理請求"""
        
        logger.info("使用第一層：搜尋引擎處理請求")
        
        # 調用 Cloud Search MCP
        search_params = {
            "query": user_input,
            "keywords": intent_result.search_keywords,
            "context": context,
            "max_results": 10
        }
        
        # 模擬搜尋結果
        return {
            "layer": "search_engine",
            "search_results": [
                {"title": "相關文檔1", "content": "搜尋到的相關內容...", "relevance": 0.9},
                {"title": "相關文檔2", "content": "更多相關信息...", "relevance": 0.8}
            ],
            "answer": f"根據搜尋結果，關於 '{user_input}' 的回答是...",
            "confidence": intent_result.confidence
        }
    
    async def _process_with_workflow_mcps(self, user_input: str, intent_result: IntentAnalysisResult, context: Dict[str, Any]) -> Dict[str, Any]:
        """使用工作流 MCP 處理請求"""
        
        logger.info(f"使用第二層：{intent_result.workflow_type.value} 工作流處理請求")
        
        # 獲取對應的工作流 MCP
        workflow_mcp_name = f"{intent_result.workflow_type.value}_mcp"
        
        # 調用對應的工作流 MCP
        workflow_params = {
            "task": user_input,
            "context": context,
            "workflow_type": intent_result.workflow_type.value,
            "auxiliary_tools": self._get_required_auxiliary_tools(intent_result.workflow_type)
        }
        
        # 模擬工作流處理結果
        return {
            "layer": "workflow_mcps",
            "workflow_type": intent_result.workflow_type.value,
            "workflow_result": {
                "status": "completed",
                "deliverables": [
                    f"{intent_result.workflow_type.value} 分析報告",
                    f"{intent_result.workflow_type.value} 實施方案"
                ],
                "next_steps": ["進入下一個工作流階段", "進行質量檢查"]
            },
            "confidence": intent_result.confidence
        }
    
    async def _process_with_kilocode_fallback(self, user_input: str, intent_result: IntentAnalysisResult, context: Dict[str, Any]) -> Dict[str, Any]:
        """使用 KiloCode 兜底處理請求"""
        
        logger.info("使用第三層：KiloCode 兜底處理請求")
        
        # 調用 KiloCode MCP 創建自定義解決方案
        kilocode_params = {
            "problem_description": user_input,
            "context": context,
            "complexity_score": intent_result.complexity_score,
            "previous_attempts": "前兩層無法解決",
            "create_new_tool": True
        }
        
        # 模擬 KiloCode 處理結果
        return {
            "layer": "kilocode_fallback",
            "solution_type": "custom_tool_creation",
            "created_tools": [
                {
                    "tool_name": f"CustomSolution_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "description": f"為 '{user_input}' 創建的自定義解決方案",
                    "capabilities": ["問題分析", "解決方案生成", "結果驗證"]
                }
            ],
            "implementation_plan": [
                "分析問題需求",
                "設計解決方案架構", 
                "實現核心功能",
                "測試和優化",
                "部署和監控"
            ],
            "confidence": 1.0  # KiloCode 總是有信心解決問題
        }
    
    def _get_required_auxiliary_tools(self, workflow_type: WorkflowType) -> List[str]:
        """獲取工作流所需的輔助工具"""
        
        # 根據工作流類型返回所需的輔助工具
        tool_mapping = {
            WorkflowType.REQUIREMENTS_ANALYSIS: ["sequential_thinking_mcp", "cloud_search_mcp"],
            WorkflowType.ARCHITECTURE_DESIGN: ["sequential_thinking_mcp", "enhanced_smartui_mcp"],
            WorkflowType.CODING_IMPLEMENTATION: ["local_model_mcp", "enhanced_smartui_mcp"],
            WorkflowType.TESTING_VALIDATION: ["cloud_edge_data_mcp", "rl_srt_mcp"],
            WorkflowType.DEPLOYMENT_OPERATIONS: ["cloud_edge_data_mcp", "enhanced_smartui_mcp"],
            WorkflowType.MAINTENANCE_SUPPORT: ["rl_srt_mcp", "cloud_edge_data_mcp"]
        }
        
        return tool_mapping.get(workflow_type, [])
    
    def get_system_status(self) -> Dict[str, Any]:
        """獲取系統狀態"""
        
        return {
            "system_name": self.name,
            "architecture": "三層漸進式處理",
            "layers": {
                "layer_1": "Cloud Search MCP (搜尋引擎)",
                "layer_2": "Six Workflow MCPs (專業工作流)",
                "layer_3": "KiloCode MCP (兜底創建)"
            },
            "available_mcps": len([mcp for mcp in self.mcp_tools.values() if mcp["status"] == "available"]),
            "processing_stats": self.processing_stats,
            "status": "operational"
        }

# 測試函數
async def test_progressive_intent_matcher():
    """測試三層漸進式意圖匹配引擎"""
    
    matcher = ProgressiveIntentMatcher()
    
    # 測試案例
    test_cases = [
        "什麼是人工智能？",  # 應該走搜尋引擎
        "我想開發一個貪吃蛇遊戲",  # 應該走編碼工作流
        "幫我創建一個全新的量子計算模擬器"  # 應該走 KiloCode 兜底
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n=== 測試案例 {i}: {test_input} ===")
        
        result = await matcher.process_request(test_input)
        
        print(f"處理結果: {result['status']}")
        print(f"使用層級: {result['processing_info']['layer_used']}")
        if result['processing_info']['workflow_type']:
            print(f"工作流類型: {result['processing_info']['workflow_type']}")
        print(f"信心度: {result['processing_info']['confidence']:.2f}")
        print(f"推理: {result['processing_info']['reasoning']}")
        print(f"處理時間: {result['processing_info']['processing_time']:.3f}秒")
    
    # 顯示系統狀態
    print(f"\n=== 系統狀態 ===")
    status = matcher.get_system_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    print("🚀 三層漸進式智能意圖匹配引擎")
    print("架構：搜尋引擎 → 六大工作流 → KiloCode 兜底")
    print("=" * 50)
    
    asyncio.run(test_progressive_intent_matcher())

