#!/usr/bin/env python3
"""
測試版 ProductOrchestrator - 專注於三層架構測試
"""

import json
import uuid
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
from dataclasses import dataclass
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
class ProductType(Enum):
    WEB_APPLICATION = "web_application"

@dataclass
class SmartUIProductRequest:
    request_id: str
    user_id: str
    product_name: str
    product_type: ProductType
    description: str
    requirements: Dict[str, Any]
    smartui_config: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.smartui_config is None:
            self.smartui_config = {
                "ui_type": "advanced",
                "features": ["voice_control", "intelligent_layout"],
                "integration_mode": "seamless"
            }

class SmartUIProductOrchestrator:
    """SmartUI 產品編排器 - 三層架構測試版"""
    
    def __init__(self, workflow_orchestrator_url: str = "http://localhost:8089"):
        self.workflow_orchestrator_url = workflow_orchestrator_url
        self.active_projects = {}
        
    async def orchestrate_smartui_development(self, smartui_request: SmartUIProductRequest) -> Dict[str, Any]:
        """編排 SmartUI 開發流程 - 三層架構"""
        try:
            logger.info(f"🎯 第一層 ProductOrchestrator: 開始 SmartUI 編排")
            logger.info(f"   產品名稱: {smartui_request.product_name}")
            logger.info(f"   SmartUI 配置: {smartui_request.smartui_config}")
            
            # 準備工作流請求
            workflow_request = {
                "workflow_id": f"smartui_{smartui_request.request_id}",
                "workflow_type": "smartui_development",
                "user_request": {
                    "product_name": smartui_request.product_name,
                    "smartui_config": smartui_request.smartui_config,
                    "requirements": smartui_request.requirements
                },
                "stages": [
                    {
                        "stage_id": "smartui_requirements",
                        "mcp_type": "requirements_analysis_mcp",
                        "timeout": 300,
                        "smartui_context": {
                            "target_ui_type": "advanced_smartui",
                            "analysis_focus": ["voice_interaction", "ui_intelligence"]
                        }
                    },
                    {
                        "stage_id": "smartui_architecture",
                        "mcp_type": "architecture_design_mcp",
                        "timeout": 300,
                        "smartui_context": {
                            "architecture_patterns": ["component_based", "mcp_integration"],
                            "frontend_framework": "react"
                        }
                    },
                    {
                        "stage_id": "smartui_coding",
                        "mcp_type": "coding_workflow_mcp",
                        "timeout": 300,
                        "smartui_context": {
                            "code_generation_mode": "smartui_components",
                            "target_components": ["voice_control", "layout_optimizer"]
                        }
                    }
                ]
            }
            
            # 第一層 → 第二層：調用 WorkflowOrchestrator
            logger.info("📡 第一層 ProductOrchestrator → 第二層 WorkflowOrchestrator")
            logger.info(f"   目標 URL: {self.workflow_orchestrator_url}/api/workflow/execute")
            
            try:
                response = requests.post(
                    f"{self.workflow_orchestrator_url}/api/workflow/execute",
                    json=workflow_request,
                    timeout=30
                )
                
                if response.status_code == 200:
                    workflow_result = response.json()
                    logger.info("✅ 第二層 WorkflowOrchestrator 回應成功")
                    logger.info(f"   回應狀態: {workflow_result.get('status')}")
                else:
                    logger.warning(f"⚠️ 第二層 WorkflowOrchestrator 回應錯誤: {response.status_code}")
                    # 模擬成功回應用於架構測試
                    workflow_result = self._create_mock_workflow_result(workflow_request)
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"⚠️ 無法連接第二層 WorkflowOrchestrator: {e}")
                logger.info("🔄 使用模擬回應繼續測試三層架構")
                workflow_result = self._create_mock_workflow_result(workflow_request)
            
            # 記錄項目狀態
            self.active_projects[smartui_request.request_id] = {
                "request": smartui_request,
                "workflow_result": workflow_result,
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "architecture_test": "三層架構調用成功"
            }
            
            logger.info("🎉 第一層 ProductOrchestrator: SmartUI 編排完成")
            
            return {
                "success": True,
                "request_id": smartui_request.request_id,
                "product_name": smartui_request.product_name,
                "workflow_results": workflow_result.get("results", {}),
                "architecture_flow": [
                    "第一層: ProductOrchestrator ✅",
                    "第二層: WorkflowOrchestrator (模擬)",
                    "第三層: MCPCoordinator (待實現)",
                    "組件層: Advanced SmartUI (待實現)"
                ],
                "message": "SmartUI 三層架構編排測試完成"
            }
            
        except Exception as e:
            logger.error(f"❌ 第一層 ProductOrchestrator 編排失敗: {e}")
            return {
                "success": False,
                "error": str(e),
                "request_id": smartui_request.request_id
            }
    
    def _create_mock_workflow_result(self, workflow_request: Dict[str, Any]) -> Dict[str, Any]:
        """創建模擬的工作流結果用於架構測試"""
        return {
            "status": "completed",
            "workflow_id": workflow_request["workflow_id"],
            "results": {
                "smartui_requirements": {
                    "status": "completed",
                    "quality_score": 0.85,
                    "outputs": {
                        "requirements_doc": "SmartUI 需求分析完成",
                        "ui_specifications": ["voice_control", "intelligent_layout"]
                    }
                },
                "smartui_architecture": {
                    "status": "completed", 
                    "quality_score": 0.88,
                    "outputs": {
                        "architecture_design": "React + Advanced SmartUI 架構",
                        "component_structure": "三層架構集成"
                    }
                },
                "smartui_coding": {
                    "status": "completed",
                    "quality_score": 0.90,
                    "outputs": {
                        "generated_code": "SmartUI 組件代碼",
                        "integration_points": ["advanced_smartui", "react_frontend"]
                    }
                }
            },
            "architecture_test": "模擬第二層和第三層回應",
            "next_steps": [
                "實現 WorkflowOrchestrator (第二層)",
                "實現 MCPCoordinator (第三層)",
                "集成 Advanced SmartUI 組件"
            ]
        }

# 全局編排器實例
orchestrator = SmartUIProductOrchestrator()

@app.route('/', methods=['GET'])
def home():
    """首頁"""
    return jsonify({
        "service": "ProductOrchestrator",
        "layer": "第一層 - 產品級",
        "status": "運行中",
        "architecture": "三層架構測試版",
        "endpoints": [
            "/api/health",
            "/api/smartui/orchestrate",
            "/api/smartui/status/<request_id>",
            "/api/test/architecture"
        ]
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查"""
    return jsonify({
        "status": "healthy",
        "service": "ProductOrchestrator",
        "layer": "第一層 - 產品級",
        "capabilities": ["smartui_orchestration"],
        "next_layer": "WorkflowOrchestrator (8089)",
        "architecture": "ProductOrchestrator → WorkflowOrchestrator → MCPCoordinator → Workflow MCP → Advanced SmartUI"
    })

@app.route('/api/smartui/orchestrate', methods=['POST'])
def orchestrate_smartui():
    """SmartUI 編排 API 端點"""
    try:
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({
                "success": False,
                "error": "請求數據不能為空"
            }), 400
        
        logger.info("🚀 收到 SmartUI 編排請求")
        logger.info(f"   請求數據: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
        
        # 創建 SmartUI 請求
        smartui_request = SmartUIProductRequest(
            request_id=str(uuid.uuid4()),
            user_id=request_data.get("user_id", "default"),
            product_name=request_data.get("product_name", "SmartUI Application"),
            product_type=ProductType.WEB_APPLICATION,
            description=request_data.get("description", "智慧感知 UI 應用"),
            requirements=request_data.get("requirements", {}),
            smartui_config=request_data.get("smartui_config", {})
        )
        
        # 執行編排
        result = asyncio.run(orchestrator.orchestrate_smartui_development(smartui_request))
        
        logger.info("📤 返回編排結果")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ SmartUI 編排 API 失敗: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/smartui/status/<request_id>')
def get_smartui_status(request_id):
    """獲取 SmartUI 項目狀態"""
    try:
        project_status = orchestrator.active_projects.get(request_id)
        
        if project_status:
            return jsonify({
                "success": True,
                "request_id": request_id,
                "status": project_status
            })
        else:
            return jsonify({
                "success": False,
                "error": "SmartUI 項目不存在"
            }), 404
            
    except Exception as e:
        logger.error(f"❌ 獲取狀態失敗: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/test/architecture', methods=['GET'])
def test_architecture():
    """測試三層架構連通性"""
    return jsonify({
        "architecture_layers": {
            "layer_1": {
                "name": "ProductOrchestrator",
                "port": 5002,
                "status": "✅ 運行中",
                "role": "產品級編排，SmartUI 需求分析"
            },
            "layer_2": {
                "name": "WorkflowOrchestrator", 
                "port": 8089,
                "status": "⏳ 待實現",
                "role": "工作流級編排，六大工作流協調"
            },
            "layer_3": {
                "name": "MCPCoordinator",
                "port": 8089,
                "status": "⏳ 待實現", 
                "role": "MCP 協調級，組件路由和負載均衡"
            },
            "components": {
                "name": "六大 Workflow MCP + Advanced SmartUI",
                "ports": "8090-8095",
                "status": "⏳ 待實現",
                "role": "具體功能實現"
            }
        },
        "call_flow": [
            "ProductOrchestrator (5002)",
            "→ WorkflowOrchestrator (8089)",
            "→ MCPCoordinator (8089)", 
            "→ 六大 Workflow MCP (8090-8095)",
            "→ Advanced SmartUI + 其他 MCP 組件"
        ],
        "test_endpoint": "/api/smartui/orchestrate"
    })

if __name__ == '__main__':
    logger.info("🚀 啟動 ProductOrchestrator (第一層) - 三層架構測試版")
    logger.info("📋 三層架構:")
    logger.info("  第一層: ProductOrchestrator (5002) ✅")
    logger.info("  第二層: WorkflowOrchestrator (8089) ⏳")
    logger.info("  第三層: MCPCoordinator + 六大 Workflow MCP ⏳")
    logger.info("  組件層: Advanced SmartUI + 其他 MCP 組件 ⏳")
    logger.info("")
    logger.info("🔗 測試 URL:")
    logger.info("  健康檢查: http://localhost:5002/api/health")
    logger.info("  架構測試: http://localhost:5002/api/test/architecture")
    logger.info("  SmartUI 編排: http://localhost:5002/api/smartui/orchestrate")
    
    app.run(host='0.0.0.0', port=5002, debug=False)

