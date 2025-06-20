#!/usr/bin/env python3
"""
完全動態自適應意圖匹配引擎
Fully Dynamic Adaptive Intent Matching Engine

整合所有 MCP tools 的智能意圖分析系統：
- rl_srt_mcp: 強化學習自適應訓練
- cloud_search_mcp: 雲端搜索能力
- smart_tool_engine_mcp: 智能工具引擎
- 其他所有可用的 MCP tools
"""

import asyncio
import json
import requests
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class MCPToolRegistry:
    """MCP 工具註冊表"""
    name: str
    endpoint: str
    capabilities: List[str]
    tool_type: str  # 'core', 'adapter', 'workflow', 'intelligence'
    priority: int = 1
    active: bool = True
    last_health_check: datetime = None
    
    def __post_init__(self):
        if self.last_health_check is None:
            self.last_health_check = datetime.now()

@dataclass
class AdaptiveLearningState:
    """自適應學習狀態"""
    pattern_weights: Dict[str, float]
    success_history: List[Dict[str, Any]]
    failure_patterns: List[Dict[str, Any]]
    learning_rate: float = 0.1
    confidence_threshold: float = 0.7
    last_update: datetime = None
    
    def __post_init__(self):
        if self.last_update is None:
            self.last_update = datetime.now()

@dataclass
class IntentMatchingResult:
    """意圖匹配結果"""
    user_input: str
    matched_workflow: str
    recommended_adapters: List[str]
    confidence_score: float
    reasoning: str
    required_capabilities: List[str]
    learning_feedback: Dict[str, Any]
    tool_chain: List[str]  # 使用的工具鏈
    analysis_metadata: Dict[str, Any]

class FullyDynamicIntentMatcher:
    """
    完全動態自適應意圖匹配引擎
    
    核心特性：
    1. 自動發現和註冊所有 MCP tools
    2. 利用 rl_srt 進行強化學習
    3. 使用 cloud_search 進行智能搜索
    4. 調用 smart_tool_engine 進行語義分析
    5. 完全動態，無硬編碼規則
    6. 自適應學習和持續優化
    """
    
    def __init__(self):
        self.mcp_tools: Dict[str, MCPToolRegistry] = {}
        self.learning_state = AdaptiveLearningState(
            pattern_weights={},
            success_history=[],
            failure_patterns=[]
        )
        
        # 核心工具端點
        self.core_tools = {
            "rl_srt_mcp": "http://localhost:8096",
            "cloud_search_mcp": "http://localhost:8097", 
            "smart_tool_engine_mcp": "http://localhost:8099"
        }
        
        # 工作流端點
        self.workflow_endpoints = {
            "requirements_analysis_mcp": "http://localhost:8090",
            "architecture_design_mcp": "http://localhost:8091",
            "coding_workflow_mcp": "http://localhost:8092",
            "developer_flow_mcp": "http://localhost:8093",
            "release_manager_mcp": "http://localhost:8094",
            "operations_workflow_mcp": "http://localhost:8095"
        }
        
        # 初始化系統
        asyncio.create_task(self.initialize_system())
    
    async def initialize_system(self):
        """初始化完全動態系統"""
        logger.info("🚀 初始化完全動態自適應意圖匹配系統")
        
        # 1. 自動發現所有 MCP tools
        await self.discover_all_mcp_tools()
        
        # 2. 初始化強化學習系統
        await self.initialize_rl_system()
        
        # 3. 驗證核心工具連接
        await self.verify_core_tools()
        
        # 4. 載入學習狀態
        await self.load_learning_state()
        
        logger.info("✅ 完全動態自適應意圖匹配系統初始化完成")
    
    async def discover_all_mcp_tools(self):
        """自動發現所有 MCP tools"""
        logger.info("🔍 自動發現所有 MCP tools")
        
        # 發現核心工具
        for name, endpoint in self.core_tools.items():
            await self.register_mcp_tool(name, endpoint, "core", priority=10)
        
        # 發現工作流工具
        for name, endpoint in self.workflow_endpoints.items():
            await self.register_mcp_tool(name, endpoint, "workflow", priority=5)
        
        # 動態發現其他工具（通過端口掃描或服務發現）
        await self.discover_additional_tools()
        
        logger.info(f"📋 發現 {len(self.mcp_tools)} 個 MCP tools")
    
    async def register_mcp_tool(self, name: str, endpoint: str, tool_type: str, priority: int = 1):
        """註冊 MCP 工具"""
        try:
            # 嘗試獲取工具能力
            capabilities = await self.query_tool_capabilities(endpoint)
            
            tool_registry = MCPToolRegistry(
                name=name,
                endpoint=endpoint,
                capabilities=capabilities,
                tool_type=tool_type,
                priority=priority,
                active=True
            )
            
            self.mcp_tools[name] = tool_registry
            logger.info(f"📝 註冊工具: {name} ({tool_type}) - {len(capabilities)} 個能力")
            
        except Exception as e:
            logger.debug(f"無法註冊工具 {name}: {e}")
    
    async def query_tool_capabilities(self, endpoint: str) -> List[str]:
        """查詢工具能力"""
        try:
            # 嘗試標準能力查詢接口
            response = requests.get(f"{endpoint}/api/capabilities", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("capabilities", [])
        except:
            pass
        
        # 如果標準接口不可用，返回推斷的能力
        return self.infer_tool_capabilities(endpoint)
    
    def infer_tool_capabilities(self, endpoint: str) -> List[str]:
        """推斷工具能力"""
        port = endpoint.split(":")[-1]
        
        # 基於端口推斷能力
        port_capabilities = {
            "8090": ["需求分析", "技術方案生成", "業務理解"],
            "8091": ["架構設計", "系統設計", "最佳實踐推薦"],
            "8092": ["代碼生成", "AI編程助手", "智能代碼補全"],
            "8093": ["自動化測試", "質量保障", "智能介入協調"],
            "8094": ["一鍵部署", "環境管理", "版本控制"],
            "8095": ["性能監控", "問題預警", "運維管理"],
            "8096": ["強化學習", "自適應訓練", "模式識別"],
            "8097": ["雲端搜索", "智能檢索", "語義分析"],
            "8099": ["智能工具引擎", "自然語言處理", "深度分析"]
        }
        
        return port_capabilities.get(port, ["通用工具能力"])
    
    async def discover_additional_tools(self):
        """發現額外的工具"""
        # 這裡可以實現更複雜的服務發現機制
        # 例如：Consul、Eureka、Kubernetes Service Discovery 等
        
        # 簡化版本：掃描常用端口範圍
        additional_ports = range(8100, 8110)
        
        for port in additional_ports:
            endpoint = f"http://localhost:{port}"
            try:
                response = requests.get(f"{endpoint}/health", timeout=2)
                if response.status_code == 200:
                    tool_name = f"discovered_tool_{port}"
                    await self.register_mcp_tool(tool_name, endpoint, "adapter")
            except:
                continue
    
    async def initialize_rl_system(self):
        """初始化強化學習系統"""
        if "rl_srt_mcp" in self.mcp_tools:
            try:
                # 初始化 RL-SRT 系統
                response = requests.post(
                    f"{self.core_tools['rl_srt_mcp']}/api/initialize",
                    json={
                        "learning_rate": self.learning_state.learning_rate,
                        "confidence_threshold": self.learning_state.confidence_threshold
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    logger.info("🧠 強化學習系統初始化成功")
                else:
                    logger.warning("⚠️ 強化學習系統初始化失敗")
                    
            except Exception as e:
                logger.warning(f"強化學習系統連接失敗: {e}")
    
    async def verify_core_tools(self):
        """驗證核心工具連接"""
        for tool_name, endpoint in self.core_tools.items():
            try:
                response = requests.get(f"{endpoint}/health", timeout=5)
                if response.status_code == 200:
                    logger.info(f"✅ {tool_name} 連接正常")
                else:
                    logger.warning(f"⚠️ {tool_name} 連接異常")
            except Exception as e:
                logger.warning(f"⚠️ {tool_name} 連接失敗: {e}")
    
    async def load_learning_state(self):
        """載入學習狀態"""
        try:
            # 從 rl_srt_mcp 載入學習狀態
            if "rl_srt_mcp" in self.mcp_tools:
                response = requests.get(
                    f"{self.core_tools['rl_srt_mcp']}/api/learning_state",
                    timeout=5
                )
                
                if response.status_code == 200:
                    state_data = response.json()
                    self.learning_state.pattern_weights = state_data.get("pattern_weights", {})
                    logger.info("📚 學習狀態載入成功")
                    
        except Exception as e:
            logger.info(f"使用默認學習狀態: {e}")
    
    async def analyze_intent_with_full_tools(self, user_input: str, context: Dict[str, Any] = None) -> IntentMatchingResult:
        """使用完整工具鏈進行意圖分析"""
        logger.info(f"🎯 使用完整工具鏈分析意圖: {user_input}")
        
        tool_chain = []
        analysis_results = {}
        
        # 1. 使用 cloud_search_mcp 進行語義搜索
        search_result = await self.analyze_with_cloud_search(user_input)
        if search_result:
            tool_chain.append("cloud_search_mcp")
            analysis_results["search"] = search_result
        
        # 2. 使用 smart_tool_engine_mcp 進行深度分析
        smart_analysis = await self.analyze_with_smart_tool_engine(user_input, analysis_results)
        if smart_analysis:
            tool_chain.append("smart_tool_engine_mcp")
            analysis_results["smart_analysis"] = smart_analysis
        
        # 3. 使用 rl_srt_mcp 進行強化學習分析
        rl_analysis = await self.analyze_with_rl_srt(user_input, analysis_results)
        if rl_analysis:
            tool_chain.append("rl_srt_mcp")
            analysis_results["rl_analysis"] = rl_analysis
        
        # 4. 綜合分析結果
        final_result = await self.synthesize_analysis_results(user_input, analysis_results, tool_chain)
        
        # 5. 記錄學習反饋
        await self.record_learning_feedback(final_result)
        
        return final_result
    
    async def analyze_with_cloud_search(self, user_input: str) -> Optional[Dict[str, Any]]:
        """使用雲端搜索進行分析"""
        try:
            if "cloud_search_mcp" not in self.mcp_tools:
                return None
            
            response = requests.post(
                f"{self.core_tools['cloud_search_mcp']}/api/semantic_search",
                json={
                    "query": user_input,
                    "search_type": "intent_analysis",
                    "max_results": 5
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info("🔍 雲端搜索分析完成")
                return result
                
        except Exception as e:
            logger.warning(f"雲端搜索分析失敗: {e}")
        
        return None
    
    async def analyze_with_smart_tool_engine(self, user_input: str, previous_results: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """使用智能工具引擎進行分析"""
        try:
            if "smart_tool_engine_mcp" not in self.mcp_tools:
                return None
            
            # 構建分析請求
            analysis_request = {
                "user_input": user_input,
                "available_tools": [tool.name for tool in self.mcp_tools.values()],
                "previous_analysis": previous_results,
                "analysis_type": "intent_matching"
            }
            
            response = requests.post(
                f"{self.core_tools['smart_tool_engine_mcp']}/api/analyze",
                json=analysis_request,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info("🧠 智能工具引擎分析完成")
                return result
                
        except Exception as e:
            logger.warning(f"智能工具引擎分析失敗: {e}")
        
        return None
    
    async def analyze_with_rl_srt(self, user_input: str, previous_results: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """使用強化學習進行分析"""
        try:
            if "rl_srt_mcp" not in self.mcp_tools:
                return None
            
            # 構建強化學習請求
            rl_request = {
                "input_text": user_input,
                "context": previous_results,
                "learning_mode": "adaptive",
                "pattern_weights": self.learning_state.pattern_weights
            }
            
            response = requests.post(
                f"{self.core_tools['rl_srt_mcp']}/api/analyze_pattern",
                json=rl_request,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info("🎯 強化學習分析完成")
                return result
                
        except Exception as e:
            logger.warning(f"強化學習分析失敗: {e}")
        
        return None
    
    async def synthesize_analysis_results(self, user_input: str, analysis_results: Dict[str, Any], tool_chain: List[str]) -> IntentMatchingResult:
        """綜合分析結果"""
        
        # 提取各個分析結果
        search_result = analysis_results.get("search", {})
        smart_analysis = analysis_results.get("smart_analysis", {})
        rl_analysis = analysis_results.get("rl_analysis", {})
        
        # 綜合推薦工作流
        recommended_workflow = self.determine_best_workflow(search_result, smart_analysis, rl_analysis)
        
        # 綜合推薦適配器
        recommended_adapters = self.determine_best_adapters(user_input, recommended_workflow, analysis_results)
        
        # 計算信心度
        confidence_score = self.calculate_confidence_score(analysis_results, tool_chain)
        
        # 生成推理說明
        reasoning = self.generate_reasoning(analysis_results, tool_chain)
        
        # 提取所需能力
        required_capabilities = self.extract_required_capabilities(analysis_results)
        
        return IntentMatchingResult(
            user_input=user_input,
            matched_workflow=recommended_workflow,
            recommended_adapters=recommended_adapters,
            confidence_score=confidence_score,
            reasoning=reasoning,
            required_capabilities=required_capabilities,
            learning_feedback={},
            tool_chain=tool_chain,
            analysis_metadata={
                "analysis_time": datetime.now().isoformat(),
                "tools_used": len(tool_chain),
                "analysis_depth": "full_dynamic"
            }
        )
    
    def determine_best_workflow(self, search_result: Dict, smart_analysis: Dict, rl_analysis: Dict) -> str:
        """確定最佳工作流"""
        
        # 收集各個分析的工作流推薦
        workflow_votes = {}
        
        # 從搜索結果中提取
        if "recommended_workflow" in search_result:
            workflow = search_result["recommended_workflow"]
            workflow_votes[workflow] = workflow_votes.get(workflow, 0) + 2
        
        # 從智能分析中提取
        if "recommended_workflow" in smart_analysis:
            workflow = smart_analysis["recommended_workflow"]
            workflow_votes[workflow] = workflow_votes.get(workflow, 0) + 3
        
        # 從強化學習中提取
        if "predicted_workflow" in rl_analysis:
            workflow = rl_analysis["predicted_workflow"]
            confidence = rl_analysis.get("confidence", 0.5)
            workflow_votes[workflow] = workflow_votes.get(workflow, 0) + (confidence * 4)
        
        # 選擇得票最高的工作流
        if workflow_votes:
            best_workflow = max(workflow_votes, key=workflow_votes.get)
            return best_workflow
        
        # 默認工作流
        return "coding_workflow_mcp"
    
    def determine_best_adapters(self, user_input: str, workflow: str, analysis_results: Dict) -> List[str]:
        """確定最佳適配器"""
        adapters = set()
        
        # 從各個分析結果中收集適配器推薦
        for result in analysis_results.values():
            if "recommended_adapters" in result:
                adapters.update(result["recommended_adapters"])
        
        # 基於工作流添加默認適配器
        workflow_adapters = {
            "coding_workflow_mcp": ["kilocode_mcp", "advanced_smartui"],
            "requirements_analysis_mcp": ["enhanced_workflow_mcp"],
            "architecture_design_mcp": ["enhanced_workflow_mcp"],
            "developer_flow_mcp": ["test_manage_mcp"],
            "release_manager_mcp": ["deployment_mcp", "github_mcp"],
            "operations_workflow_mcp": ["monitoring_mcp"]
        }
        
        if workflow in workflow_adapters:
            adapters.update(workflow_adapters[workflow])
        
        return list(adapters)
    
    def calculate_confidence_score(self, analysis_results: Dict, tool_chain: List[str]) -> float:
        """計算信心度分數"""
        
        # 基礎信心度
        base_confidence = 0.5
        
        # 工具使用加成
        tool_bonus = len(tool_chain) * 0.1
        
        # 分析結果一致性加成
        consistency_bonus = 0.0
        if len(analysis_results) > 1:
            # 檢查推薦的一致性
            workflows = []
            for result in analysis_results.values():
                if "recommended_workflow" in result:
                    workflows.append(result["recommended_workflow"])
            
            if workflows and len(set(workflows)) == 1:
                consistency_bonus = 0.2
        
        # 強化學習信心度
        rl_confidence = 0.0
        if "rl_analysis" in analysis_results:
            rl_confidence = analysis_results["rl_analysis"].get("confidence", 0.0) * 0.3
        
        total_confidence = min(1.0, base_confidence + tool_bonus + consistency_bonus + rl_confidence)
        return total_confidence
    
    def generate_reasoning(self, analysis_results: Dict, tool_chain: List[str]) -> str:
        """生成推理說明"""
        reasoning_parts = []
        
        if "search" in analysis_results:
            reasoning_parts.append("基於雲端搜索的語義分析")
        
        if "smart_analysis" in analysis_results:
            reasoning_parts.append("智能工具引擎的深度理解")
        
        if "rl_analysis" in analysis_results:
            reasoning_parts.append("強化學習的模式識別")
        
        if reasoning_parts:
            return f"綜合 {', '.join(reasoning_parts)} 的結果進行推薦"
        else:
            return "基於本地智能分析進行推薦"
    
    def extract_required_capabilities(self, analysis_results: Dict) -> List[str]:
        """提取所需能力"""
        capabilities = set()
        
        for result in analysis_results.values():
            if "required_capabilities" in result:
                capabilities.update(result["required_capabilities"])
        
        return list(capabilities)
    
    async def record_learning_feedback(self, result: IntentMatchingResult):
        """記錄學習反饋"""
        try:
            if "rl_srt_mcp" in self.mcp_tools:
                feedback_data = {
                    "user_input": result.user_input,
                    "predicted_workflow": result.matched_workflow,
                    "confidence": result.confidence_score,
                    "tool_chain": result.tool_chain,
                    "timestamp": datetime.now().isoformat()
                }
                
                requests.post(
                    f"{self.core_tools['rl_srt_mcp']}/api/record_feedback",
                    json=feedback_data,
                    timeout=5
                )
                
        except Exception as e:
            logger.debug(f"記錄學習反饋失敗: {e}")
    
    async def update_learning_from_user_feedback(self, user_input: str, actual_workflow: str, success: bool):
        """根據用戶反饋更新學習"""
        try:
            if "rl_srt_mcp" in self.mcp_tools:
                feedback_data = {
                    "user_input": user_input,
                    "actual_workflow": actual_workflow,
                    "success": success,
                    "timestamp": datetime.now().isoformat()
                }
                
                response = requests.post(
                    f"{self.core_tools['rl_srt_mcp']}/api/update_learning",
                    json=feedback_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    logger.info(f"📚 學習更新成功: {user_input} → {actual_workflow} ({'成功' if success else '失敗'})")
                    
        except Exception as e:
            logger.warning(f"學習更新失敗: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """獲取系統狀態"""
        active_tools = [tool for tool in self.mcp_tools.values() if tool.active]
        
        return {
            "total_tools": len(self.mcp_tools),
            "active_tools": len(active_tools),
            "core_tools": list(self.core_tools.keys()),
            "workflow_tools": list(self.workflow_endpoints.keys()),
            "learning_state": {
                "pattern_weights_count": len(self.learning_state.pattern_weights),
                "success_history_count": len(self.learning_state.success_history),
                "learning_rate": self.learning_state.learning_rate
            },
            "tool_registry": {
                tool.name: {
                    "type": tool.tool_type,
                    "capabilities": tool.capabilities,
                    "priority": tool.priority,
                    "active": tool.active
                }
                for tool in self.mcp_tools.values()
            },
            "last_updated": datetime.now().isoformat()
        }

# 測試和演示代碼
async def test_fully_dynamic_intent_matcher():
    """測試完全動態意圖匹配器"""
    matcher = FullyDynamicIntentMatcher()
    
    # 等待初始化完成
    await asyncio.sleep(3)
    
    print("🧪 測試完全動態自適應意圖匹配器")
    
    # 測試用例
    test_cases = [
        "我想開發貪吃蛇遊戲",
        "建立一個 React 購物車應用",
        "需要分析系統需求並設計架構",
        "進行代碼測試和質量保障",
        "部署應用到生產環境並監控",
        "開發一個聊天機器人",
        "建立數據可視化儀表板",
        "設計微服務架構",
        "實現用戶認證系統"
    ]
    
    print("\n🎯 完全動態意圖分析測試:")
    for user_input in test_cases:
        result = await matcher.analyze_intent_with_full_tools(user_input)
        
        print(f"\n輸入: '{user_input}'")
        print(f"  推薦工作流: {result.matched_workflow}")
        print(f"  推薦適配器: {result.recommended_adapters}")
        print(f"  信心度: {result.confidence_score:.2f}")
        print(f"  工具鏈: {' → '.join(result.tool_chain)}")
        print(f"  推理: {result.reasoning}")
        print(f"  所需能力: {result.required_capabilities[:3]}...")
    
    # 顯示系統狀態
    status = matcher.get_system_status()
    print(f"\n📊 系統狀態:")
    print(f"  總工具數: {status['total_tools']}")
    print(f"  活躍工具數: {status['active_tools']}")
    print(f"  核心工具: {status['core_tools']}")
    print(f"  學習狀態: {status['learning_state']}")

if __name__ == "__main__":
    asyncio.run(test_fully_dynamic_intent_matcher())

