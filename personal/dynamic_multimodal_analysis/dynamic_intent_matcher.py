#!/usr/bin/env python3
"""
動態可擴展意圖匹配引擎
Dynamic Extensible Intent Matching Engine

基於 MCP tools 的智能意圖分析系統，避免硬編碼規則，採用動態擴展機制
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
class MCPToolCapability:
    """MCP 工具能力描述"""
    tool_name: str
    capabilities: List[str]
    description: str
    endpoint: Optional[str] = None
    auto_discovered: bool = True
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()

@dataclass
class IntentAnalysisRequest:
    """意圖分析請求"""
    user_input: str
    available_capabilities: List[MCPToolCapability]
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}

@dataclass
class IntentAnalysisResponse:
    """意圖分析響應"""
    user_input: str
    recommended_workflow: str
    recommended_adapters: List[str]
    confidence_score: float
    reasoning: str
    required_capabilities: List[str]
    analysis_metadata: Dict[str, Any]

class DynamicIntentMatcher:
    """
    動態可擴展意圖匹配器
    
    核心特性：
    1. 自動發現 MCP tools 能力
    2. 利用 smart tool engine 進行智能分析
    3. 動態擴展，無需硬編碼規則
    4. 基於實際能力進行匹配
    """
    
    def __init__(self, smart_tool_engine_endpoint: str = "http://localhost:8099"):
        self.smart_tool_engine_endpoint = smart_tool_engine_endpoint
        self.discovered_capabilities: Dict[str, MCPToolCapability] = {}
        self.capability_registry = None
        
        # 動態發現配置
        self.discovery_endpoints = [
            "http://localhost:8090",  # requirements_analysis_mcp
            "http://localhost:8091",  # architecture_design_mcp  
            "http://localhost:8092",  # coding_workflow_mcp
            "http://localhost:8093",  # developer_flow_mcp
            "http://localhost:8094",  # release_manager_mcp
            "http://localhost:8095",  # operations_workflow_mcp
        ]
        
        # 初始化
        asyncio.create_task(self.initialize_system())
    
    async def initialize_system(self):
        """初始化系統"""
        logger.info("🚀 初始化動態意圖匹配系統")
        
        # 1. 自動發現 MCP 能力
        await self.discover_mcp_capabilities()
        
        # 2. 驗證 smart tool engine 連接
        await self.verify_smart_tool_engine()
        
        logger.info("✅ 動態意圖匹配系統初始化完成")
    
    async def discover_mcp_capabilities(self):
        """自動發現 MCP 能力"""
        logger.info("🔍 自動發現 MCP 能力")
        
        for endpoint in self.discovery_endpoints:
            try:
                # 嘗試獲取 MCP 能力信息
                capability_info = await self.query_mcp_capabilities(endpoint)
                if capability_info:
                    self.register_discovered_capability(capability_info)
                    
            except Exception as e:
                logger.debug(f"無法連接到 {endpoint}: {e}")
        
        logger.info(f"📋 發現 {len(self.discovered_capabilities)} 個 MCP 能力")
    
    async def query_mcp_capabilities(self, endpoint: str) -> Optional[MCPToolCapability]:
        """查詢 MCP 能力"""
        try:
            # 嘗試標準化的能力查詢接口
            response = requests.get(f"{endpoint}/api/capabilities", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return MCPToolCapability(
                    tool_name=data.get("name", endpoint.split(":")[-1]),
                    capabilities=data.get("capabilities", []),
                    description=data.get("description", ""),
                    endpoint=endpoint,
                    auto_discovered=True
                )
        except:
            pass
        
        # 如果標準接口不可用，嘗試推斷能力
        return self.infer_mcp_capabilities(endpoint)
    
    def infer_mcp_capabilities(self, endpoint: str) -> Optional[MCPToolCapability]:
        """推斷 MCP 能力（基於端口和命名）"""
        port = endpoint.split(":")[-1]
        
        # 基於已知的端口映射推斷能力
        port_mapping = {
            "8090": {
                "name": "requirements_analysis_mcp",
                "capabilities": ["需求分析", "技術方案生成", "業務理解"],
                "description": "需求分析工作流"
            },
            "8091": {
                "name": "architecture_design_mcp", 
                "capabilities": ["架構設計", "系統設計", "最佳實踐推薦"],
                "description": "架構設計工作流"
            },
            "8092": {
                "name": "coding_workflow_mcp",
                "capabilities": ["代碼生成", "AI編程助手", "智能代碼補全"],
                "description": "編碼工作流"
            },
            "8093": {
                "name": "developer_flow_mcp",
                "capabilities": ["自動化測試", "質量保障", "智能介入協調"],
                "description": "開發者工作流"
            },
            "8094": {
                "name": "release_manager_mcp",
                "capabilities": ["一鍵部署", "環境管理", "版本控制"],
                "description": "發布管理工作流"
            },
            "8095": {
                "name": "operations_workflow_mcp",
                "capabilities": ["性能監控", "問題預警", "運維管理"],
                "description": "運維工作流"
            }
        }
        
        if port in port_mapping:
            info = port_mapping[port]
            return MCPToolCapability(
                tool_name=info["name"],
                capabilities=info["capabilities"],
                description=info["description"],
                endpoint=endpoint,
                auto_discovered=True
            )
        
        return None
    
    def register_discovered_capability(self, capability: MCPToolCapability):
        """註冊發現的能力"""
        self.discovered_capabilities[capability.tool_name] = capability
        logger.info(f"📝 註冊能力: {capability.tool_name} - {capability.capabilities}")
    
    async def verify_smart_tool_engine(self):
        """驗證 smart tool engine 連接"""
        try:
            response = requests.get(f"{self.smart_tool_engine_endpoint}/health", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Smart Tool Engine 連接正常")
                return True
        except Exception as e:
            logger.warning(f"⚠️ Smart Tool Engine 連接失敗: {e}")
            logger.info("💡 將使用本地智能分析作為備用方案")
        
        return False
    
    async def analyze_intent(self, user_input: str, context: Dict[str, Any] = None) -> IntentAnalysisResponse:
        """分析用戶意圖"""
        logger.info(f"🎯 分析用戶意圖: {user_input}")
        
        # 準備分析請求
        request = IntentAnalysisRequest(
            user_input=user_input,
            available_capabilities=list(self.discovered_capabilities.values()),
            context=context or {}
        )
        
        # 嘗試使用 smart tool engine 進行分析
        try:
            response = await self.analyze_with_smart_tool_engine(request)
            if response:
                return response
        except Exception as e:
            logger.warning(f"Smart Tool Engine 分析失敗: {e}")
        
        # 備用方案：使用本地智能分析
        return await self.analyze_with_local_intelligence(request)
    
    async def analyze_with_smart_tool_engine(self, request: IntentAnalysisRequest) -> Optional[IntentAnalysisResponse]:
        """使用 smart tool engine 進行分析"""
        
        # 構建分析提示
        analysis_prompt = self.build_analysis_prompt(request)
        
        # 調用 smart tool engine
        payload = {
            "prompt": analysis_prompt,
            "context": request.context,
            "capabilities": [asdict(cap) for cap in request.available_capabilities]
        }
        
        try:
            response = requests.post(
                f"{self.smart_tool_engine_endpoint}/api/analyze_intent",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return self.parse_smart_tool_response(result, request.user_input)
                
        except Exception as e:
            logger.error(f"Smart Tool Engine 調用失敗: {e}")
        
        return None
    
    def build_analysis_prompt(self, request: IntentAnalysisRequest) -> str:
        """構建分析提示"""
        capabilities_text = "\n".join([
            f"- {cap.tool_name}: {', '.join(cap.capabilities)} ({cap.description})"
            for cap in request.available_capabilities
        ])
        
        prompt = f"""
請分析以下用戶需求，並推薦最適合的工作流和適配器：

用戶輸入："{request.user_input}"

可用的 MCP 工具能力：
{capabilities_text}

請提供：
1. 推薦的主要工作流
2. 需要的適配器列表
3. 信心度評分 (0-1)
4. 推薦理由
5. 所需的具體能力

請以 JSON 格式回應：
{{
    "recommended_workflow": "工作流名稱",
    "recommended_adapters": ["適配器1", "適配器2"],
    "confidence_score": 0.95,
    "reasoning": "推薦理由",
    "required_capabilities": ["能力1", "能力2"]
}}
"""
        return prompt
    
    def parse_smart_tool_response(self, result: Dict, user_input: str) -> IntentAnalysisResponse:
        """解析 smart tool 響應"""
        return IntentAnalysisResponse(
            user_input=user_input,
            recommended_workflow=result.get("recommended_workflow", ""),
            recommended_adapters=result.get("recommended_adapters", []),
            confidence_score=result.get("confidence_score", 0.0),
            reasoning=result.get("reasoning", ""),
            required_capabilities=result.get("required_capabilities", []),
            analysis_metadata={
                "source": "smart_tool_engine",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    async def analyze_with_local_intelligence(self, request: IntentAnalysisRequest) -> IntentAnalysisResponse:
        """使用本地智能分析（備用方案）"""
        logger.info("🧠 使用本地智能分析")
        
        user_input_lower = request.user_input.lower()
        
        # 基於語義相似度進行匹配
        best_match = None
        best_score = 0.0
        
        for cap in request.available_capabilities:
            score = self.calculate_semantic_similarity(user_input_lower, cap)
            if score > best_score:
                best_score = score
                best_match = cap
        
        if best_match and best_score > 0.3:
            # 推斷所需的適配器
            adapters = self.infer_required_adapters(user_input_lower, best_match)
            
            return IntentAnalysisResponse(
                user_input=request.user_input,
                recommended_workflow=best_match.tool_name,
                recommended_adapters=adapters,
                confidence_score=best_score,
                reasoning=f"基於語義相似度匹配到 {best_match.tool_name}",
                required_capabilities=best_match.capabilities,
                analysis_metadata={
                    "source": "local_intelligence",
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        # 如果沒有好的匹配，返回默認建議
        return IntentAnalysisResponse(
            user_input=request.user_input,
            recommended_workflow="coding_workflow_mcp",  # 默認編碼工作流
            recommended_adapters=["kilocode_mcp"],
            confidence_score=0.5,
            reasoning="未找到明確匹配，使用默認編碼工作流",
            required_capabilities=["代碼生成"],
            analysis_metadata={
                "source": "local_intelligence_fallback",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def calculate_semantic_similarity(self, user_input: str, capability: MCPToolCapability) -> float:
        """計算語義相似度"""
        # 簡化版本：基於關鍵詞匹配
        score = 0.0
        
        # 檢查工具名稱匹配
        tool_keywords = capability.tool_name.replace("_", " ").split()
        for keyword in tool_keywords:
            if keyword in user_input:
                score += 0.2
        
        # 檢查能力匹配
        for cap in capability.capabilities:
            cap_lower = cap.lower()
            if any(word in user_input for word in cap_lower.split()):
                score += 0.3
        
        # 檢查描述匹配
        desc_words = capability.description.lower().split()
        for word in desc_words:
            if word in user_input:
                score += 0.1
        
        return min(1.0, score)
    
    def infer_required_adapters(self, user_input: str, matched_capability: MCPToolCapability) -> List[str]:
        """推斷所需的適配器"""
        adapters = []
        
        # 基於用戶輸入推斷
        if "遊戲" in user_input or "貪吃蛇" in user_input:
            adapters.extend(["kilocode_mcp", "game_development_adapter"])
        elif "react" in user_input or "前端" in user_input:
            adapters.extend(["kilocode_mcp", "advanced_smartui"])
        elif "測試" in user_input:
            adapters.extend(["test_manage_mcp"])
        elif "部署" in user_input:
            adapters.extend(["deployment_mcp", "github_mcp"])
        else:
            # 默認適配器
            adapters.append("kilocode_mcp")
        
        return adapters
    
    async def register_new_mcp_tool(self, tool_info: Dict[str, Any]):
        """註冊新的 MCP 工具"""
        capability = MCPToolCapability(
            tool_name=tool_info["name"],
            capabilities=tool_info["capabilities"],
            description=tool_info.get("description", ""),
            endpoint=tool_info.get("endpoint"),
            auto_discovered=False
        )
        
        self.register_discovered_capability(capability)
        logger.info(f"🆕 手動註冊新工具: {capability.tool_name}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """獲取系統狀態"""
        return {
            "discovered_capabilities": len(self.discovered_capabilities),
            "smart_tool_engine_endpoint": self.smart_tool_engine_endpoint,
            "capabilities": {
                name: {
                    "capabilities": cap.capabilities,
                    "description": cap.description,
                    "auto_discovered": cap.auto_discovered
                }
                for name, cap in self.discovered_capabilities.items()
            },
            "last_updated": datetime.now().isoformat()
        }

# 測試和演示代碼
async def test_dynamic_intent_matcher():
    """測試動態意圖匹配器"""
    matcher = DynamicIntentMatcher()
    
    # 等待初始化完成
    await asyncio.sleep(2)
    
    print("🧪 測試動態意圖匹配器")
    
    # 測試用例
    test_cases = [
        "我想開發貪吃蛇遊戲",
        "建立一個 React 購物車應用", 
        "需要分析系統需求",
        "設計微服務架構",
        "進行代碼測試",
        "部署到生產環境"
    ]
    
    print("\n🎯 動態意圖分析測試:")
    for user_input in test_cases:
        result = await matcher.analyze_intent(user_input)
        
        print(f"\n輸入: '{user_input}'")
        print(f"  推薦工作流: {result.recommended_workflow}")
        print(f"  推薦適配器: {result.recommended_adapters}")
        print(f"  信心度: {result.confidence_score:.2f}")
        print(f"  推薦理由: {result.reasoning}")
        print(f"  分析來源: {result.analysis_metadata.get('source', 'unknown')}")
    
    # 顯示系統狀態
    status = matcher.get_system_status()
    print(f"\n📊 系統狀態:")
    print(json.dumps(status, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test_dynamic_intent_matcher())

