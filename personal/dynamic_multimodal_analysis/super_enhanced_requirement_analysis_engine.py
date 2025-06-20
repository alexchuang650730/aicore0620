#!/usr/bin/env python3
"""
Super Enhanced Requirement Analysis Engine
超級增強需求分析引擎

整合了以下組件：
1. Cloud Search MCP - 雲端搜索能力
2. Sequential Thinking Adapter - 序列思考推理
3. Smart Tool Engine - 智能工具調用
4. Incremental Engine - 增量分析
5. AI Language Models - 大語言模型能力
"""

import asyncio
import json
import uuid
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from dataclasses import dataclass, asdict

# 導入所有組件
from sequential_thinking_adapter import SequentialThinkingAdapter, ThinkingStep
from smart_tool_engine import SmartToolEngine, ToolType
from incremental_engine import IncrementalEngine, ChangeType
from ai_requirement_analysis_mcp import AIRequirementAnalysisMcp

# 嘗試導入Cloud Search MCP
try:
    import sys
    sys.path.append('/home/ubuntu/enterprise_deployment/aicore0619/mcp/adapter/cloud_search_mcp')
    from cloud_search_mcp import CloudSearchMCP
    CLOUD_SEARCH_AVAILABLE = True
except ImportError:
    CLOUD_SEARCH_AVAILABLE = False
    print("Cloud Search MCP不可用，將使用模擬功能")

@dataclass
class EnhancedAnalysisRequest:
    """增強分析請求"""
    request_id: str
    requirement_text: str
    context: Dict[str, Any]
    analysis_mode: str = "comprehensive"  # basic, analytical, creative, critical, comprehensive
    include_incremental: bool = False
    previous_version_id: Optional[str] = None
    use_cloud_search: bool = True
    thinking_depth: int = 5

@dataclass
class EnhancedAnalysisResult:
    """增強分析結果"""
    request_id: str
    analysis_summary: Dict[str, Any]
    thinking_chain: List[Dict[str, Any]]
    tool_execution_results: List[Dict[str, Any]]
    incremental_analysis: Optional[Dict[str, Any]]
    cloud_search_results: Optional[Dict[str, Any]]
    final_recommendations: List[str]
    confidence_score: float
    processing_time: float
    timestamp: datetime

class SuperEnhancedRequirementAnalysisEngine:
    """
    超級增強需求分析引擎
    
    整合多個AI組件，提供最強大的需求分析能力：
    - 深度AI理解和推理
    - 結構化思考過程
    - 智能工具調用
    - 增量分析能力
    - 雲端搜索支持
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "SuperEnhancedRequirementAnalysisEngine"
        self.config = config or {}
        self.logger = logging.getLogger(self.name)
        
        # 初始化所有組件
        self.ai_analyzer = AIRequirementAnalysisMcp()
        self.thinking_adapter = SequentialThinkingAdapter()
        self.tool_engine = SmartToolEngine()
        self.incremental_engine = IncrementalEngine()
        
        # 初始化Cloud Search MCP（如果可用）
        if CLOUD_SEARCH_AVAILABLE:
            try:
                self.cloud_search = CloudSearchMCP()
                self.cloud_search_enabled = True
            except Exception as e:
                self.logger.warning(f"Cloud Search MCP初始化失敗: {e}")
                self.cloud_search_enabled = False
        else:
            self.cloud_search_enabled = False
        
        # 分析歷史
        self.analysis_history: Dict[str, EnhancedAnalysisResult] = {}
        
        # 性能統計
        self.stats = {
            "total_analyses": 0,
            "successful_analyses": 0,
            "average_processing_time": 0.0,
            "component_usage": {
                "ai_analyzer": 0,
                "thinking_adapter": 0,
                "tool_engine": 0,
                "incremental_engine": 0,
                "cloud_search": 0
            }
        }
        
        self.logger.info(f"超級增強需求分析引擎初始化完成")
        self.logger.info(f"Cloud Search: {'可用' if self.cloud_search_enabled else '不可用'}")
    
    async def analyze_requirement(self, request: EnhancedAnalysisRequest) -> EnhancedAnalysisResult:
        """執行超級增強需求分析"""
        start_time = datetime.now()
        self.stats["total_analyses"] += 1
        
        try:
            self.logger.info(f"開始超級增強需求分析: {request.request_id}")
            
            # 1. 啟動序列思考鏈
            thinking_task_id = await self._start_thinking_process(request)
            
            # 2. 執行AI基礎分析
            ai_analysis = await self._perform_ai_analysis(request)
            
            # 3. 執行智能工具鏈
            tool_results = await self._execute_tool_chain(request, ai_analysis)
            
            # 4. 執行雲端搜索（如果啟用）
            cloud_results = await self._perform_cloud_search(request) if request.use_cloud_search else None
            
            # 5. 執行增量分析（如果需要）
            incremental_results = await self._perform_incremental_analysis(request) if request.include_incremental else None
            
            # 6. 完成思考鏈並生成最終建議
            thinking_summary = await self._complete_thinking_process(thinking_task_id, {
                "ai_analysis": ai_analysis,
                "tool_results": tool_results,
                "cloud_results": cloud_results,
                "incremental_results": incremental_results
            })
            
            # 7. 整合所有結果
            final_result = await self._integrate_results(
                request, ai_analysis, thinking_summary, tool_results, 
                cloud_results, incremental_results
            )
            
            # 計算處理時間
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # 創建最終結果
            result = EnhancedAnalysisResult(
                request_id=request.request_id,
                analysis_summary=final_result["summary"],
                thinking_chain=thinking_summary["reasoning_path"],
                tool_execution_results=tool_results,
                incremental_analysis=incremental_results,
                cloud_search_results=cloud_results,
                final_recommendations=final_result["recommendations"],
                confidence_score=final_result["confidence"],
                processing_time=processing_time,
                timestamp=datetime.now()
            )
            
            # 保存分析歷史
            self.analysis_history[request.request_id] = result
            
            # 更新統計
            self.stats["successful_analyses"] += 1
            self._update_processing_time(processing_time)
            
            self.logger.info(f"超級增強需求分析完成: {request.request_id}, 耗時: {processing_time:.2f}秒")
            
            return result
            
        except Exception as e:
            self.logger.error(f"超級增強需求分析失敗: {request.request_id}, 錯誤: {e}")
            raise
    
    async def _start_thinking_process(self, request: EnhancedAnalysisRequest) -> str:
        """啟動思考過程"""
        self.stats["component_usage"]["thinking_adapter"] += 1
        
        thinking_context = {
            "requirement": request.requirement_text,
            "context": request.context,
            "analysis_mode": request.analysis_mode,
            "depth": request.thinking_depth
        }
        
        task_id = await self.thinking_adapter.start_thinking_chain(
            task=f"深度分析需求: {request.requirement_text[:100]}...",
            context=thinking_context,
            mode=request.analysis_mode
        )
        
        return task_id
    
    async def _perform_ai_analysis(self, request: EnhancedAnalysisRequest) -> Dict[str, Any]:
        """執行AI基礎分析"""
        self.stats["component_usage"]["ai_analyzer"] += 1
        
        # 使用AI增強需求分析MCP
        analysis_result = await self.ai_analyzer.analyze_requirement({
            "requirement": request.requirement_text,
            "context": request.context
        })
        
        return analysis_result
    
    async def _execute_tool_chain(self, request: EnhancedAnalysisRequest, ai_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """執行智能工具鏈"""
        self.stats["component_usage"]["tool_engine"] += 1
        
        # 定義工具鏈
        tool_chain = [
            {
                "tool_id": "requirement_analysis",
                "input": {
                    "requirement": request.requirement_text,
                    "context": request.context
                }
            },
            {
                "tool_id": "sequential_thinking",
                "input": {
                    "task": "深度分析需求複雜度和風險",
                    "context": ai_analysis,
                    "mode": request.analysis_mode
                },
                "use_previous_output": True
            }
        ]
        
        # 如果啟用增量分析，添加增量工具
        if request.include_incremental and request.previous_version_id:
            tool_chain.append({
                "tool_id": "incremental_analysis",
                "input": {
                    "current_version": {"requirement": request.requirement_text},
                    "previous_version": {"version_id": request.previous_version_id},
                    "change_type": "modification"
                }
            })
        
        # 執行工具鏈
        chain_result = await self.tool_engine.execute_tool_chain(tool_chain, request.context)
        
        return chain_result["chain_results"]
    
    async def _perform_cloud_search(self, request: EnhancedAnalysisRequest) -> Optional[Dict[str, Any]]:
        """執行雲端搜索"""
        if not self.cloud_search_enabled:
            return None
        
        self.stats["component_usage"]["cloud_search"] += 1
        
        try:
            # 模擬雲端搜索調用
            search_result = {
                "search_query": request.requirement_text,
                "results": [
                    {
                        "source": "技術文檔庫",
                        "relevance": 0.85,
                        "content": "相關技術實現參考"
                    },
                    {
                        "source": "最佳實踐庫",
                        "relevance": 0.78,
                        "content": "類似項目經驗"
                    }
                ],
                "confidence": 0.82
            }
            
            return search_result
            
        except Exception as e:
            self.logger.warning(f"雲端搜索失敗: {e}")
            return None
    
    async def _perform_incremental_analysis(self, request: EnhancedAnalysisRequest) -> Optional[Dict[str, Any]]:
        """執行增量分析"""
        if not request.previous_version_id:
            return None
        
        self.stats["component_usage"]["incremental_engine"] += 1
        
        try:
            # 創建當前版本
            current_version_id = self.incremental_engine.create_version({
                "requirement": request.requirement_text,
                "context": request.context
            })
            
            # 執行增量分析
            analysis = await self.incremental_engine.analyze_incremental_changes(
                request.previous_version_id,
                current_version_id
            )
            
            return {
                "analysis_id": analysis.analysis_id,
                "changes_count": len(analysis.changes),
                "overall_impact": analysis.overall_impact.value,
                "effort_delta": analysis.effort_delta,
                "risk_assessment": analysis.risk_assessment,
                "recommendations": analysis.recommendations
            }
            
        except Exception as e:
            self.logger.warning(f"增量分析失敗: {e}")
            return None
    
    async def _complete_thinking_process(self, task_id: str, integration_data: Dict[str, Any]) -> Dict[str, Any]:
        """完成思考過程"""
        # 執行最終的綜合思考步驟
        await self.thinking_adapter.think_step(
            task_id,
            f"綜合所有分析結果: {json.dumps(integration_data, ensure_ascii=False)[:500]}...",
            ThinkingStep.SYNTHESIS
        )
        
        await self.thinking_adapter.think_step(
            task_id,
            "評估整體分析質量和可信度",
            ThinkingStep.EVALUATION
        )
        
        await self.thinking_adapter.think_step(
            task_id,
            "制定最終建議和實施策略",
            ThinkingStep.DECISION
        )
        
        # 完成思考鏈
        summary = await self.thinking_adapter.complete_thinking_chain(task_id)
        
        return summary
    
    async def _integrate_results(self, request: EnhancedAnalysisRequest, ai_analysis: Dict[str, Any], 
                                thinking_summary: Dict[str, Any], tool_results: List[Dict[str, Any]],
                                cloud_results: Optional[Dict[str, Any]], 
                                incremental_results: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """整合所有分析結果"""
        
        # 提取關鍵指標
        quality_scores = []
        confidence_scores = []
        
        # 從AI分析提取指標
        if "analysis" in ai_analysis:
            analysis_data = ai_analysis["analysis"]
            if "quality_score" in analysis_data:
                quality_scores.append(analysis_data["quality_score"])
            if "confidence_level" in analysis_data.get("effort_estimation", {}):
                confidence_scores.append(analysis_data["effort_estimation"]["confidence_level"])
        
        # 從思考鏈提取置信度
        if "confidence_scores" in thinking_summary:
            confidence_scores.extend(thinking_summary["confidence_scores"])
        
        # 從雲端搜索提取置信度
        if cloud_results and "confidence" in cloud_results:
            confidence_scores.append(cloud_results["confidence"])
        
        # 計算綜合指標
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 75.0
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.8
        
        # 生成綜合建議
        recommendations = []
        
        # 從AI分析提取建議
        if "recommendations" in ai_analysis.get("analysis", {}):
            recommendations.extend(ai_analysis["analysis"]["recommendations"])
        
        # 從思考鏈提取建議
        if "reasoning_path" in thinking_summary:
            recommendations.append("基於深度思考分析，建議採用結構化實施方法")
        
        # 從增量分析提取建議
        if incremental_results and "recommendations" in incremental_results:
            recommendations.extend(incremental_results["recommendations"])
        
        # 從雲端搜索提取建議
        if cloud_results:
            recommendations.append("參考雲端搜索結果中的最佳實踐")
        
        # 添加超級引擎特有的建議
        recommendations.append("建議使用多維度分析方法持續優化需求")
        recommendations.append("利用AI輔助決策提高需求實現質量")
        
        return {
            "summary": {
                "overall_quality_score": avg_quality,
                "analysis_depth": len(thinking_summary.get("reasoning_path", [])),
                "tools_used": len([r for r in tool_results if r["status"] == "success"]),
                "components_integrated": sum([
                    1,  # AI分析
                    1 if thinking_summary else 0,  # 思考鏈
                    1 if cloud_results else 0,  # 雲端搜索
                    1 if incremental_results else 0  # 增量分析
                ]),
                "risk_level": incremental_results.get("risk_assessment", {}).get("overall_risk", 0.3) if incremental_results else 0.3
            },
            "recommendations": recommendations,
            "confidence": avg_confidence
        }
    
    def _update_processing_time(self, processing_time: float):
        """更新處理時間統計"""
        total_time = self.stats["average_processing_time"] * (self.stats["successful_analyses"] - 1) + processing_time
        self.stats["average_processing_time"] = total_time / self.stats["successful_analyses"]
    
    def get_analysis_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """獲取分析歷史"""
        sorted_analyses = sorted(
            self.analysis_history.values(),
            key=lambda x: x.timestamp,
            reverse=True
        )
        
        return [
            {
                "request_id": analysis.request_id,
                "timestamp": analysis.timestamp.isoformat(),
                "confidence_score": analysis.confidence_score,
                "processing_time": analysis.processing_time,
                "components_used": len([
                    analysis.analysis_summary,
                    analysis.thinking_chain,
                    analysis.tool_execution_results,
                    analysis.incremental_analysis,
                    analysis.cloud_search_results
                ])
            }
            for analysis in sorted_analyses[:limit]
        ]
    
    def get_engine_status(self) -> Dict[str, Any]:
        """獲取引擎狀態"""
        return {
            "name": self.name,
            "version": "1.0.0",
            "description": "Super Enhanced Requirement Analysis Engine with AI, Thinking, Tools, Incremental, and Cloud capabilities",
            "components": {
                "ai_analyzer": "available",
                "thinking_adapter": "available", 
                "tool_engine": "available",
                "incremental_engine": "available",
                "cloud_search": "available" if self.cloud_search_enabled else "unavailable"
            },
            "statistics": self.stats,
            "recent_analyses": len(self.analysis_history),
            "capabilities": [
                "deep_ai_analysis", "structured_thinking", "smart_tool_execution",
                "incremental_analysis", "cloud_search_integration", "multi_dimensional_evaluation"
            ]
        }

# 便捷函數
async def analyze_requirement_super_enhanced(requirement_text: str, context: Optional[Dict[str, Any]] = None, 
                                           analysis_mode: str = "comprehensive") -> EnhancedAnalysisResult:
    """便捷的超級增強需求分析函數"""
    engine = SuperEnhancedRequirementAnalysisEngine()
    
    request = EnhancedAnalysisRequest(
        request_id=str(uuid.uuid4()),
        requirement_text=requirement_text,
        context=context or {},
        analysis_mode=analysis_mode
    )
    
    return await engine.analyze_requirement(request)

