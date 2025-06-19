#!/usr/bin/env python3
"""
WorkflowOrchestrator - 第二層工作流編排器
負責接收 ProductOrchestrator 的請求，協調六大工作流的執行
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
class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class StageStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class WorkflowStage:
    stage_id: str
    mcp_type: str
    timeout: int
    smartui_context: Dict[str, Any]
    template: Optional[str] = None
    depends_on: List[str] = None
    status: StageStatus = StageStatus.PENDING
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    quality_score: Optional[float] = None
    results: Optional[Dict] = None
    error_message: Optional[str] = None

@dataclass
class WorkflowInstance:
    workflow_id: str
    workflow_type: str
    user_request: Dict[str, Any]
    stages: List[WorkflowStage]
    status: WorkflowStatus = WorkflowStatus.PENDING
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    current_stage: Optional[str] = None
    results: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.results is None:
            self.results = {}

class WorkflowOrchestrator:
    """第二層工作流編排器"""
    
    def __init__(self, mcp_coordinator_url: str = "http://localhost:8089"):
        self.mcp_coordinator_url = mcp_coordinator_url
        self.active_workflows = {}
        self.workflow_templates = self._load_workflow_templates()
        
    def _load_workflow_templates(self) -> Dict[str, Any]:
        """載入工作流模板"""
        return {
            "smartui_development": {
                "description": "SmartUI 智慧感知 UI 開發工作流",
                "stages": [
                    {
                        "stage_id": "smartui_requirements",
                        "mcp_type": "requirements_analysis_mcp",
                        "port": 8090,
                        "description": "SmartUI 需求分析",
                        "expected_outputs": ["requirements_doc", "ui_specifications"]
                    },
                    {
                        "stage_id": "smartui_architecture", 
                        "mcp_type": "architecture_design_mcp",
                        "port": 8091,
                        "description": "SmartUI 架構設計",
                        "expected_outputs": ["architecture_design", "component_structure"]
                    },
                    {
                        "stage_id": "smartui_coding",
                        "mcp_type": "coding_workflow_mcp",
                        "port": 8092,
                        "description": "SmartUI 編碼實現",
                        "expected_outputs": ["generated_code", "integration_points"]
                    },
                    {
                        "stage_id": "smartui_testing",
                        "mcp_type": "developer_flow_mcp",
                        "port": 8093,
                        "description": "SmartUI 測試驗證",
                        "expected_outputs": ["test_results", "quality_metrics"]
                    },
                    {
                        "stage_id": "smartui_deployment",
                        "mcp_type": "release_manager_mcp",
                        "port": 8094,
                        "description": "SmartUI 部署發布",
                        "expected_outputs": ["deployment_status", "service_urls"]
                    },
                    {
                        "stage_id": "smartui_monitoring",
                        "mcp_type": "operations_workflow_mcp",
                        "port": 8095,
                        "description": "SmartUI 監控運維",
                        "expected_outputs": ["monitoring_setup", "alert_config"]
                    }
                ]
            }
        }
    
    async def execute_workflow(self, workflow_request: Dict[str, Any]) -> Dict[str, Any]:
        """執行工作流 - 第二層核心功能"""
        try:
            workflow_id = workflow_request.get("workflow_id")
            workflow_type = workflow_request.get("workflow_type")
            
            logger.info(f"🎯 第二層 WorkflowOrchestrator: 開始執行工作流")
            logger.info(f"   工作流 ID: {workflow_id}")
            logger.info(f"   工作流類型: {workflow_type}")
            
            # 創建工作流實例
            workflow_instance = self._create_workflow_instance(workflow_request)
            self.active_workflows[workflow_id] = workflow_instance
            
            # 執行工作流階段
            workflow_result = await self._execute_workflow_stages(workflow_instance)
            
            # 更新工作流狀態
            workflow_instance.status = WorkflowStatus.COMPLETED if workflow_result["success"] else WorkflowStatus.FAILED
            workflow_instance.end_time = datetime.now().isoformat()
            workflow_instance.results = workflow_result.get("results", {})
            
            logger.info(f"🎉 第二層 WorkflowOrchestrator: 工作流執行完成")
            logger.info(f"   執行狀態: {workflow_instance.status.value}")
            
            return {
                "status": workflow_instance.status.value,
                "workflow_id": workflow_id,
                "results": workflow_instance.results,
                "execution_summary": {
                    "total_stages": len(workflow_instance.stages),
                    "completed_stages": len([s for s in workflow_instance.stages if s.status == StageStatus.COMPLETED]),
                    "start_time": workflow_instance.start_time,
                    "end_time": workflow_instance.end_time
                }
            }
            
        except Exception as e:
            logger.error(f"❌ 第二層 WorkflowOrchestrator 執行失敗: {e}")
            return {
                "status": "failed",
                "error_message": str(e),
                "workflow_id": workflow_request.get("workflow_id")
            }
    
    def _create_workflow_instance(self, workflow_request: Dict[str, Any]) -> WorkflowInstance:
        """創建工作流實例"""
        stages = []
        for stage_data in workflow_request.get("stages", []):
            stage = WorkflowStage(
                stage_id=stage_data["stage_id"],
                mcp_type=stage_data["mcp_type"],
                timeout=stage_data.get("timeout", 300),
                smartui_context=stage_data.get("smartui_context", {}),
                template=stage_data.get("template"),
                depends_on=stage_data.get("depends_on", [])
            )
            stages.append(stage)
        
        return WorkflowInstance(
            workflow_id=workflow_request["workflow_id"],
            workflow_type=workflow_request["workflow_type"],
            user_request=workflow_request.get("user_request", {}),
            stages=stages,
            start_time=datetime.now().isoformat()
        )
    
    async def _execute_workflow_stages(self, workflow_instance: WorkflowInstance) -> Dict[str, Any]:
        """執行工作流階段"""
        results = {}
        
        for stage in workflow_instance.stages:
            try:
                logger.info(f"📡 第二層 → 第三層: 執行階段 {stage.stage_id}")
                
                # 檢查依賴
                if not self._check_stage_dependencies(stage, results):
                    stage.status = StageStatus.FAILED
                    stage.error_message = "依賴階段未完成"
                    continue
                
                # 準備 MCPCoordinator 請求
                mcp_request = {
                    "stage_id": stage.stage_id,
                    "mcp_type": stage.mcp_type,
                    "user_request": workflow_instance.user_request,
                    "smartui_context": stage.smartui_context,
                    "template": stage.template,
                    "previous_results": results
                }
                
                # 調用第三層 MCPCoordinator
                stage_result = await self._call_mcp_coordinator(mcp_request)
                
                # 處理階段結果
                if stage_result.get("success"):
                    stage.status = StageStatus.COMPLETED
                    stage.quality_score = stage_result.get("quality_score", 0.8)
                    stage.results = stage_result.get("outputs", {})
                    results[stage.stage_id] = stage.results
                    logger.info(f"✅ 階段 {stage.stage_id} 完成，品質分數: {stage.quality_score}")
                else:
                    stage.status = StageStatus.FAILED
                    stage.error_message = stage_result.get("error", "階段執行失敗")
                    logger.error(f"❌ 階段 {stage.stage_id} 失敗: {stage.error_message}")
                
                stage.end_time = datetime.now().isoformat()
                
            except Exception as e:
                stage.status = StageStatus.FAILED
                stage.error_message = str(e)
                stage.end_time = datetime.now().isoformat()
                logger.error(f"❌ 階段 {stage.stage_id} 執行異常: {e}")
        
        # 檢查整體執行結果
        completed_stages = [s for s in workflow_instance.stages if s.status == StageStatus.COMPLETED]
        success = len(completed_stages) == len(workflow_instance.stages)
        
        return {
            "success": success,
            "results": results,
            "stage_summary": {
                "total": len(workflow_instance.stages),
                "completed": len(completed_stages),
                "failed": len([s for s in workflow_instance.stages if s.status == StageStatus.FAILED])
            }
        }
    
    def _check_stage_dependencies(self, stage: WorkflowStage, completed_results: Dict[str, Any]) -> bool:
        """檢查階段依賴"""
        if not stage.depends_on:
            return True
        
        for dependency in stage.depends_on:
            if dependency not in completed_results:
                return False
        
        return True
    
    async def _call_mcp_coordinator(self, mcp_request: Dict[str, Any]) -> Dict[str, Any]:
        """調用第三層 MCPCoordinator"""
        try:
            logger.info(f"📡 第二層 WorkflowOrchestrator → 第三層 MCPCoordinator")
            logger.info(f"   目標 MCP: {mcp_request['mcp_type']}")
            
            # 直接調用對應的 MCP 組件
            mcp_type = mcp_request["mcp_type"]
            stage_id = mcp_request["stage_id"]
            
            # MCP 組件端口映射
            mcp_ports = {
                "requirements_analysis_mcp": 8090,
                "architecture_design_mcp": 8091,
                "coding_workflow_mcp": 8092,
                "developer_flow_mcp": 8093,
                "release_manager_mcp": 8094,
                "operations_workflow_mcp": 8095
            }
            
            port = mcp_ports.get(mcp_type)
            if not port:
                raise Exception(f"未知的 MCP 類型: {mcp_type}")
            
            # 調用真實的 MCP 組件
            response = requests.post(
                f"http://localhost:{port}/api/execute",
                json=mcp_request,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ MCP 組件 {mcp_type} 真實調用成功")
                return result
            else:
                logger.error(f"❌ MCP 組件 {mcp_type} 回應錯誤: {response.status_code}")
                raise Exception(f"MCP 組件調用失敗: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 無法連接 MCP 組件 {mcp_type}: {e}")
            raise Exception(f"MCP 組件連接失敗: {e}")
    
    def _create_mock_mcp_result(self, mcp_request: Dict[str, Any]) -> Dict[str, Any]:
        """創建模擬的 MCP 結果"""
        stage_id = mcp_request["stage_id"]
        mcp_type = mcp_request["mcp_type"]
        
        mock_outputs = {
            "smartui_requirements": {
                "requirements_doc": f"SmartUI 需求分析文檔 - {stage_id}",
                "ui_specifications": ["voice_control", "intelligent_layout", "node_interaction"],
                "technical_requirements": "React + Advanced SmartUI 集成"
            },
            "smartui_architecture": {
                "architecture_design": f"SmartUI 系統架構設計 - {stage_id}",
                "component_structure": "三層架構 + MCP 組件集成",
                "integration_points": ["advanced_smartui", "mcp_coordinator"]
            },
            "smartui_coding": {
                "generated_code": f"SmartUI 組件代碼 - {stage_id}",
                "integration_points": ["advanced_smartui", "react_frontend"],
                "code_quality": "高品質代碼生成"
            }
        }
        
        return {
            "success": True,
            "stage_id": stage_id,
            "mcp_type": mcp_type,
            "quality_score": 0.85 + (hash(stage_id) % 10) * 0.01,  # 模擬不同的品質分數
            "outputs": mock_outputs.get(stage_id, {"result": f"模擬 {stage_id} 執行結果"}),
            "execution_time": 2.5,
            "mock_response": True
        }

# 全局編排器實例
workflow_orchestrator = WorkflowOrchestrator()

@app.route('/', methods=['GET'])
def home():
    """首頁"""
    return jsonify({
        "service": "WorkflowOrchestrator",
        "layer": "第二層 - 工作流級",
        "status": "運行中",
        "capabilities": ["workflow_execution", "stage_coordination", "mcp_integration"],
        "supported_workflows": list(workflow_orchestrator.workflow_templates.keys())
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查"""
    return jsonify({
        "status": "healthy",
        "service": "WorkflowOrchestrator",
        "layer": "第二層 - 工作流級",
        "role": "工作流編排和階段協調",
        "next_layer": "MCPCoordinator (8089)",
        "supported_workflows": len(workflow_orchestrator.workflow_templates)
    })

@app.route('/api/workflow/execute', methods=['POST'])
def execute_workflow():
    """執行工作流 - 接收第一層 ProductOrchestrator 的請求"""
    try:
        workflow_request = request.get_json()
        
        if not workflow_request:
            return jsonify({
                "success": False,
                "error": "工作流請求數據不能為空"
            }), 400
        
        logger.info("🚀 第二層 WorkflowOrchestrator: 收到工作流執行請求")
        logger.info(f"   來自第一層 ProductOrchestrator")
        logger.info(f"   工作流類型: {workflow_request.get('workflow_type')}")
        
        # 執行工作流
        result = asyncio.run(workflow_orchestrator.execute_workflow(workflow_request))
        
        logger.info("📤 第二層 WorkflowOrchestrator: 返回執行結果給第一層")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ 第二層 WorkflowOrchestrator 執行失敗: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/workflow/status/<workflow_id>')
def get_workflow_status(workflow_id):
    """獲取工作流狀態"""
    try:
        workflow_instance = workflow_orchestrator.active_workflows.get(workflow_id)
        
        if workflow_instance:
            return jsonify({
                "success": True,
                "workflow_id": workflow_id,
                "status": workflow_instance.status.value,
                "current_stage": workflow_instance.current_stage,
                "stages": [asdict(stage) for stage in workflow_instance.stages],
                "results": workflow_instance.results
            })
        else:
            return jsonify({
                "success": False,
                "error": "工作流不存在"
            }), 404
            
    except Exception as e:
        logger.error(f"❌ 獲取工作流狀態失敗: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/workflow/templates')
def get_workflow_templates():
    """獲取工作流模板"""
    return jsonify({
        "success": True,
        "templates": workflow_orchestrator.workflow_templates
    })

@app.route('/api/test/layer2', methods=['GET'])
def test_layer2():
    """測試第二層功能"""
    return jsonify({
        "layer": "第二層 - WorkflowOrchestrator",
        "status": "✅ 運行中",
        "capabilities": [
            "接收第一層 ProductOrchestrator 請求",
            "工作流模板管理",
            "階段依賴處理",
            "調用第三層 MCPCoordinator",
            "結果聚合和回傳"
        ],
        "workflow_templates": list(workflow_orchestrator.workflow_templates.keys()),
        "active_workflows": len(workflow_orchestrator.active_workflows),
        "next_layer": "MCPCoordinator (第三層)"
    })

if __name__ == '__main__':
    logger.info("🚀 啟動 WorkflowOrchestrator (第二層)")
    logger.info("📋 工作流模板:")
    for template_name, template_data in workflow_orchestrator.workflow_templates.items():
        logger.info(f"  {template_name}: {template_data['description']}")
        logger.info(f"    階段數量: {len(template_data['stages'])}")
    logger.info("")
    logger.info("🔗 API 端點:")
    logger.info("  健康檢查: http://localhost:8089/api/health")
    logger.info("  工作流執行: http://localhost:8089/api/workflow/execute")
    logger.info("  第二層測試: http://localhost:8089/api/test/layer2")
    logger.info("")
    logger.info("📡 三層架構位置:")
    logger.info("  第一層: ProductOrchestrator (5002) → 第二層: WorkflowOrchestrator (8089)")
    
    app.run(host='0.0.0.0', port=8089, debug=False)

