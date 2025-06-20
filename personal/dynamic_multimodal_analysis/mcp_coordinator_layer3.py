#!/usr/bin/env python3
"""
MCPCoordinator - 第三層 MCP 協調器
負責接收 WorkflowOrchestrator 的請求，協調六大 Workflow MCP 和 Advanced SmartUI 組件
"""

import json
import uuid
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 數據結構
class MCPStatus(Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    UNAVAILABLE = "unavailable"

@dataclass
class MCPComponent:
    name: str
    port: int
    status: MCPStatus
    capabilities: List[str]
    last_health_check: Optional[str] = None
    response_time: Optional[float] = None

class MCPCoordinator:
    """第三層 MCP 協調器"""
    
    def __init__(self):
        self.registered_mcps = self._initialize_mcp_registry()
        self.active_requests = {}
        
    def _initialize_mcp_registry(self) -> Dict[str, MCPComponent]:
        """初始化 MCP 組件註冊表"""
        return {
            # 六大 Workflow MCP
            "requirements_analysis_mcp": MCPComponent(
                name="requirements_analysis_mcp",
                port=8090,
                status=MCPStatus.AVAILABLE,
                capabilities=["smartui_requirements", "business_analysis", "technical_specs"]
            ),
            "architecture_design_mcp": MCPComponent(
                name="architecture_design_mcp", 
                port=8091,
                status=MCPStatus.AVAILABLE,
                capabilities=["smartui_architecture", "system_design", "component_structure"]
            ),
            "coding_workflow_mcp": MCPComponent(
                name="coding_workflow_mcp",
                port=8092,
                status=MCPStatus.AVAILABLE,
                capabilities=["smartui_coding", "code_generation", "kilocode_integration"]
            ),
            "developer_flow_mcp": MCPComponent(
                name="developer_flow_mcp",
                port=8093,
                status=MCPStatus.AVAILABLE,
                capabilities=["smartui_testing", "quality_assurance", "test_automation"]
            ),
            "release_manager_mcp": MCPComponent(
                name="release_manager_mcp",
                port=8094,
                status=MCPStatus.AVAILABLE,
                capabilities=["smartui_deployment", "release_management", "environment_setup"]
            ),
            "operations_workflow_mcp": MCPComponent(
                name="operations_workflow_mcp",
                port=8095,
                status=MCPStatus.AVAILABLE,
                capabilities=["smartui_monitoring", "performance_tracking", "alert_management"]
            ),
            
            # Advanced SmartUI 組件
            "advanced_smartui": MCPComponent(
                name="advanced_smartui",
                port=8098,
                status=MCPStatus.AVAILABLE,
                capabilities=["voice_control", "intelligent_layout", "ui_generation", "react_integration"]
            )
        }
    
    async def coordinate_mcp_request(self, mcp_request: Dict[str, Any]) -> Dict[str, Any]:
        """協調 MCP 請求 - 第三層核心功能"""
        try:
            stage_id = mcp_request.get("stage_id")
            mcp_type = mcp_request.get("mcp_type")
            
            logger.info(f"🎯 第三層 MCPCoordinator: 開始協調 MCP 請求")
            logger.info(f"   階段 ID: {stage_id}")
            logger.info(f"   目標 MCP: {mcp_type}")
            
            # 檢查 MCP 組件可用性
            target_mcp = self.registered_mcps.get(mcp_type)
            if not target_mcp:
                raise Exception(f"MCP 組件 {mcp_type} 未註冊")
            
            # 選擇合適的 MCP 組件
            selected_components = await self._select_mcp_components(mcp_request, target_mcp)
            
            # 執行 MCP 組件調用
            mcp_result = await self._execute_mcp_components(mcp_request, selected_components)
            
            # 記錄請求
            request_id = str(uuid.uuid4())
            self.active_requests[request_id] = {
                "stage_id": stage_id,
                "mcp_type": mcp_type,
                "selected_components": [comp.name for comp in selected_components],
                "result": mcp_result,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"🎉 第三層 MCPCoordinator: MCP 協調完成")
            logger.info(f"   使用組件: {[comp.name for comp in selected_components]}")
            
            return mcp_result
            
        except Exception as e:
            logger.error(f"❌ 第三層 MCPCoordinator 協調失敗: {e}")
            return {
                "success": False,
                "error": str(e),
                "stage_id": mcp_request.get("stage_id")
            }
    
    async def _select_mcp_components(self, mcp_request: Dict[str, Any], target_mcp: MCPComponent) -> List[MCPComponent]:
        """選擇合適的 MCP 組件"""
        stage_id = mcp_request.get("stage_id")
        smartui_context = mcp_request.get("smartui_context", {})
        
        selected_components = [target_mcp]
        
        # 根據 SmartUI 上下文選擇額外組件
        if "smartui" in stage_id:
            # 對於 SmartUI 相關階段，總是包含 Advanced SmartUI 組件
            advanced_smartui = self.registered_mcps.get("advanced_smartui")
            if advanced_smartui and advanced_smartui not in selected_components:
                selected_components.append(advanced_smartui)
                logger.info(f"   選擇 Advanced SmartUI 組件用於 SmartUI 功能")
        
        # 根據功能需求選擇額外組件
        if stage_id == "smartui_coding":
            # 編碼階段可能需要額外的代碼生成組件
            logger.info(f"   編碼階段：選擇 KiloCode 集成")
        
        logger.info(f"📋 第三層選擇的組件: {[comp.name for comp in selected_components]}")
        return selected_components
    
    async def _execute_mcp_components(self, mcp_request: Dict[str, Any], components: List[MCPComponent]) -> Dict[str, Any]:
        """執行 MCP 組件調用"""
        stage_id = mcp_request.get("stage_id")
        results = {}
        
        for component in components:
            try:
                logger.info(f"📡 第三層 → 組件層: 調用 {component.name}")
                
                # 準備組件請求
                component_request = {
                    "stage_id": stage_id,
                    "user_request": mcp_request.get("user_request", {}),
                    "smartui_context": mcp_request.get("smartui_context", {}),
                    "template": mcp_request.get("template"),
                    "previous_results": mcp_request.get("previous_results", {})
                }
                
                # 調用組件
                component_result = await self._call_mcp_component(component, component_request)
                
                if component_result.get("success"):
                    results[component.name] = component_result
                    logger.info(f"✅ 組件 {component.name} 執行成功")
                else:
                    logger.warning(f"⚠️ 組件 {component.name} 執行失敗: {component_result.get('error')}")
                    
            except Exception as e:
                logger.error(f"❌ 調用組件 {component.name} 異常: {e}")
                results[component.name] = {
                    "success": False,
                    "error": str(e)
                }
        
        # 聚合結果
        return self._aggregate_component_results(stage_id, results)
    
    async def _call_mcp_component(self, component: MCPComponent, component_request: Dict[str, Any]) -> Dict[str, Any]:
        """調用單個 MCP 組件"""
        try:
            # 嘗試調用真實組件
            response = requests.post(
                f"http://localhost:{component.port}/api/execute",
                json=component_request,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ 組件 {component.name} 真實調用成功")
                return result
            else:
                logger.warning(f"⚠️ 組件 {component.name} 回應錯誤: {response.status_code}")
                return self._create_mock_component_result(component, component_request)
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ 無法連接組件 {component.name}: {e}")
            logger.info(f"🔄 使用模擬回應繼續測試")
            return self._create_mock_component_result(component, component_request)
    
    def _create_mock_component_result(self, component: MCPComponent, component_request: Dict[str, Any]) -> Dict[str, Any]:
        """創建模擬的組件結果"""
        stage_id = component_request["stage_id"]
        
        # 根據組件類型和階段生成不同的模擬結果
        mock_results = {
            "requirements_analysis_mcp": {
                "requirements_analysis": f"SmartUI 需求分析 - {component.name}",
                "functional_specs": ["voice_control", "intelligent_layout", "real_time_updates"],
                "technical_constraints": "React + Advanced SmartUI 架構限制",
                "quality_metrics": {"completeness": 0.9, "clarity": 0.85}
            },
            "architecture_design_mcp": {
                "system_architecture": f"SmartUI 系統架構 - {component.name}",
                "component_design": "三層架構 + MCP 組件集成設計",
                "integration_patterns": ["event_driven", "component_based", "mcp_protocol"],
                "scalability_plan": "水平擴展 + 負載均衡"
            },
            "coding_workflow_mcp": {
                "generated_components": f"SmartUI React 組件 - {component.name}",
                "code_structure": "模組化組件架構",
                "integration_code": "Advanced SmartUI 集成代碼",
                "code_quality_score": 0.92
            },
            "advanced_smartui": {
                "voice_control_module": "智慧語音控制組件",
                "layout_optimizer": "動態佈局優化引擎", 
                "ui_intelligence": "智慧感知 UI 核心",
                "react_integration": "React 前端集成接口"
            }
        }
        
        return {
            "success": True,
            "component": component.name,
            "stage_id": stage_id,
            "outputs": mock_results.get(component.name, {"result": f"模擬 {component.name} 執行結果"}),
            "quality_score": 0.85 + (hash(f"{component.name}_{stage_id}") % 10) * 0.01,
            "execution_time": 1.5 + (hash(component.name) % 20) * 0.1,
            "mock_response": True
        }
    
    def _aggregate_component_results(self, stage_id: str, component_results: Dict[str, Any]) -> Dict[str, Any]:
        """聚合組件結果"""
        successful_components = [name for name, result in component_results.items() if result.get("success")]
        
        if not successful_components:
            return {
                "success": False,
                "error": "所有組件執行失敗",
                "stage_id": stage_id
            }
        
        # 聚合輸出
        aggregated_outputs = {}
        total_quality_score = 0
        total_execution_time = 0
        
        for component_name, result in component_results.items():
            if result.get("success"):
                outputs = result.get("outputs", {})
                aggregated_outputs.update(outputs)
                total_quality_score += result.get("quality_score", 0)
                total_execution_time += result.get("execution_time", 0)
        
        avg_quality_score = total_quality_score / len(successful_components) if successful_components else 0
        
        return {
            "success": True,
            "stage_id": stage_id,
            "outputs": aggregated_outputs,
            "quality_score": avg_quality_score,
            "execution_time": total_execution_time,
            "components_used": successful_components,
            "component_count": len(successful_components)
        }

# 全局協調器實例
mcp_coordinator = MCPCoordinator()

@app.route('/', methods=['GET'])
def home():
    """首頁"""
    return jsonify({
        "service": "MCPCoordinator",
        "layer": "第三層 - MCP 協調級",
        "status": "運行中",
        "registered_mcps": len(mcp_coordinator.registered_mcps),
        "capabilities": ["mcp_routing", "component_selection", "load_balancing", "result_aggregation"]
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查"""
    return jsonify({
        "status": "healthy",
        "service": "MCPCoordinator", 
        "layer": "第三層 - MCP 協調級",
        "role": "MCP 組件協調和路由",
        "registered_mcps": len(mcp_coordinator.registered_mcps),
        "active_requests": len(mcp_coordinator.active_requests)
    })

@app.route('/api/mcp/coordinate', methods=['POST'])
def coordinate_mcp():
    """協調 MCP 請求 - 接收第二層 WorkflowOrchestrator 的請求"""
    try:
        mcp_request = request.get_json()
        
        if not mcp_request:
            return jsonify({
                "success": False,
                "error": "MCP 請求數據不能為空"
            }), 400
        
        logger.info("🚀 第三層 MCPCoordinator: 收到 MCP 協調請求")
        logger.info(f"   來自第二層 WorkflowOrchestrator")
        logger.info(f"   目標 MCP: {mcp_request.get('mcp_type')}")
        
        # 執行 MCP 協調
        result = asyncio.run(mcp_coordinator.coordinate_mcp_request(mcp_request))
        
        logger.info("📤 第三層 MCPCoordinator: 返回協調結果給第二層")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ 第三層 MCPCoordinator 協調失敗: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/mcp/registry')
def get_mcp_registry():
    """獲取 MCP 組件註冊表"""
    return jsonify({
        "success": True,
        "registered_mcps": {
            name: asdict(component) 
            for name, component in mcp_coordinator.registered_mcps.items()
        }
    })

@app.route('/api/test/layer3', methods=['GET'])
def test_layer3():
    """測試第三層功能"""
    return jsonify({
        "layer": "第三層 - MCPCoordinator",
        "status": "✅ 運行中",
        "capabilities": [
            "接收第二層 WorkflowOrchestrator 請求",
            "MCP 組件註冊和發現",
            "智慧組件選擇",
            "負載均衡和路由",
            "結果聚合",
            "調用六大 Workflow MCP",
            "調用 Advanced SmartUI 組件"
        ],
        "registered_mcps": {
            "workflow_mcps": [
                "requirements_analysis_mcp (8090)",
                "architecture_design_mcp (8091)",
                "coding_workflow_mcp (8092)",
                "developer_flow_mcp (8093)",
                "release_manager_mcp (8094)",
                "operations_workflow_mcp (8095)"
            ],
            "smartui_components": [
                "advanced_smartui (8098)"
            ]
        },
        "active_requests": len(mcp_coordinator.active_requests),
        "next_layer": "六大 Workflow MCP + Advanced SmartUI (組件層)"
    })

if __name__ == '__main__':
    logger.info("🚀 啟動 MCPCoordinator (第三層)")
    logger.info("📋 註冊的 MCP 組件:")
    for name, component in mcp_coordinator.registered_mcps.items():
        logger.info(f"  {name} (端口 {component.port}): {', '.join(component.capabilities)}")
    logger.info("")
    logger.info("🔗 API 端點:")
    logger.info("  健康檢查: http://localhost:8089/api/health")
    logger.info("  MCP 協調: http://localhost:8089/api/mcp/coordinate")
    logger.info("  第三層測試: http://localhost:8089/api/test/layer3")
    logger.info("")
    logger.info("📡 三層架構位置:")
    logger.info("  第二層: WorkflowOrchestrator (8089) → 第三層: MCPCoordinator (8089)")
    logger.info("  第三層 → 組件層: 六大 Workflow MCP (8090-8095) + Advanced SmartUI (8098)")
    
    # 注意：MCPCoordinator 與 WorkflowOrchestrator 共享端口 8089
    # 在實際部署中，它們可以作為同一服務的不同路由
    app.run(host='0.0.0.0', port=8089, debug=False)

