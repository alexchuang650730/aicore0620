#!/usr/bin/env python3
"""
Personal Product Orchestrator - 個人專業版工作流編排器

使用personal目錄下的兩個AI引擎：
- dynamic_multimodal_analysis: 動態多模態分析引擎
- multimodal_requirement_analysis: 多模態需求分析引擎
"""

import asyncio
import json
import time
import uuid
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# 添加personal引擎路徑
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dynamic_multimodal_analysis'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'multimodal_requirement_analysis'))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# 1. 數據結構定義
# ============================================================================

class WorkflowType(Enum):
    """個人專業版智能工作流類型"""
    DYNAMIC_MULTIMODAL_ANALYSIS = "dynamic_multimodal_analysis"
    MULTIMODAL_REQUIREMENT_ANALYSIS = "multimodal_requirement_analysis"
    REQUIREMENT_ANALYSIS = "requirement_analysis"
    ARCHITECTURE_DESIGN = "architecture_design"
    CODING_IMPLEMENTATION = "coding_implementation"
    TESTING_VALIDATION = "testing_validation"

class WorkflowStatus(Enum):
    """工作流狀態"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ProductType(Enum):
    """產品類型"""
    WEB_APPLICATION = "web_application"
    MOBILE_APP = "mobile_app"
    API_SERVICE = "api_service"
    DESKTOP_APPLICATION = "desktop_application"
    AI_MODEL = "ai_model"

@dataclass
class ProductRequest:
    """產品開發請求"""
    request_id: str
    user_id: str
    product_name: str
    product_type: ProductType
    description: str
    requirements: Dict[str, Any]
    priority: str = "normal"
    deadline: Optional[str] = None
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

@dataclass
class WorkflowTask:
    """工作流任務"""
    task_id: str
    workflow_type: WorkflowType
    status: WorkflowStatus
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration: Optional[float] = None

@dataclass
class ProductProject:
    """產品項目"""
    project_id: str
    request: ProductRequest
    workflows: List[WorkflowTask]
    current_workflow: Optional[WorkflowType] = None
    overall_status: WorkflowStatus = WorkflowStatus.PENDING
    progress: float = 0.0
    artifacts: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.artifacts is None:
            self.artifacts = {}

# ============================================================================
# 2. Personal AI引擎接口
# ============================================================================

class PersonalAIEngineInterface:
    """Personal AI引擎接口"""
    
    def __init__(self, engine_path: str):
        self.engine_path = engine_path
        
    async def execute(self, task: WorkflowTask) -> WorkflowTask:
        """執行AI引擎任務"""
        raise NotImplementedError

class DynamicMultimodalAnalysisEngine(PersonalAIEngineInterface):
    """動態多模態分析引擎"""
    
    def __init__(self):
        super().__init__("../dynamic_multimodal_analysis")
        
    async def execute(self, task: WorkflowTask) -> WorkflowTask:
        """執行動態多模態分析"""
        logger.info(f"開始動態多模態分析任務: {task.task_id}")
        
        task.status = WorkflowStatus.RUNNING
        task.started_at = datetime.now().isoformat()
        
        try:
            # 調用動態多模態分析引擎
            from dynamic_analysis_engine import DynamicAnalysisEngine
            
            engine = DynamicAnalysisEngine()
            
            analysis_request = {
                "description": task.input_data.get("description", ""),
                "requirements": task.input_data.get("requirements", {}),
                "context": task.input_data.get("context", {})
            }
            
            result = await engine.analyze(analysis_request)
            
            if result.get("success"):
                task.output_data = {
                    "multimodal_analysis": result.get("analysis", {}),
                    "dynamic_insights": result.get("insights", []),
                    "recommendations": result.get("recommendations", []),
                    "confidence_score": result.get("confidence_score", 0),
                    "analysis_metadata": result.get("metadata", {})
                }
                task.status = WorkflowStatus.COMPLETED
            else:
                task.status = WorkflowStatus.FAILED
                task.error_message = result.get("error", "動態多模態分析失敗")
                
        except Exception as e:
            task.status = WorkflowStatus.FAILED
            task.error_message = str(e)
            logger.error(f"動態多模態分析執行失敗: {e}")
        
        task.completed_at = datetime.now().isoformat()
        return task

class MultimodalRequirementAnalysisEngine(PersonalAIEngineInterface):
    """多模態需求分析引擎"""
    
    def __init__(self):
        super().__init__("../multimodal_requirement_analysis")
        
    async def execute(self, task: WorkflowTask) -> WorkflowTask:
        """執行多模態需求分析"""
        logger.info(f"開始多模態需求分析任務: {task.task_id}")
        
        task.status = WorkflowStatus.RUNNING
        task.started_at = datetime.now().isoformat()
        
        try:
            # 調用多模態需求分析引擎
            from src.interactive_requirement_analysis_workflow_mcp import InteractiveRequirementAnalysisWorkflowMCP
            
            engine = InteractiveRequirementAnalysisWorkflowMCP()
            
            analysis_request = {
                "requirement": task.input_data.get("description", ""),
                "context": task.input_data.get("context", {}),
                "multimodal_data": task.input_data.get("multimodal_analysis", {})
            }
            
            result = await engine.analyze_requirement(analysis_request)
            
            if result.get("success"):
                task.output_data = {
                    "requirement_analysis": result.get("analysis", {}),
                    "technical_requirements": result.get("technical_requirements", {}),
                    "functional_requirements": result.get("functional_requirements", []),
                    "non_functional_requirements": result.get("non_functional_requirements", []),
                    "technology_recommendations": result.get("technology_recommendations", []),
                    "complexity_score": result.get("complexity_score", 0)
                }
                task.status = WorkflowStatus.COMPLETED
            else:
                task.status = WorkflowStatus.FAILED
                task.error_message = result.get("error", "多模態需求分析失敗")
                
        except Exception as e:
            task.status = WorkflowStatus.FAILED
            task.error_message = str(e)
            logger.error(f"多模態需求分析執行失敗: {e}")
        
        task.completed_at = datetime.now().isoformat()
        return task

# ============================================================================
# 3. Personal Product Orchestrator
# ============================================================================

class PersonalProductOrchestrator:
    """個人專業版產品編排器"""
    
    def __init__(self):
        self.projects: Dict[str, ProductProject] = {}
        
        # 初始化Personal AI引擎
        self.engines = {
            WorkflowType.DYNAMIC_MULTIMODAL_ANALYSIS: DynamicMultimodalAnalysisEngine(),
            WorkflowType.MULTIMODAL_REQUIREMENT_ANALYSIS: MultimodalRequirementAnalysisEngine()
        }
        
        logger.info("Personal Product Orchestrator 初始化完成")
        
    async def create_product(self, product_request: ProductRequest) -> str:
        """創建產品開發項目"""
        project_id = str(uuid.uuid4())
        
        # 創建Personal工作流任務序列
        workflows = [
            WorkflowTask(
                task_id=f"{project_id}_{WorkflowType.DYNAMIC_MULTIMODAL_ANALYSIS.value}",
                workflow_type=WorkflowType.DYNAMIC_MULTIMODAL_ANALYSIS,
                status=WorkflowStatus.PENDING,
                input_data={
                    "description": product_request.description,
                    "requirements": product_request.requirements,
                    "product_type": product_request.product_type.value
                }
            ),
            WorkflowTask(
                task_id=f"{project_id}_{WorkflowType.MULTIMODAL_REQUIREMENT_ANALYSIS.value}",
                workflow_type=WorkflowType.MULTIMODAL_REQUIREMENT_ANALYSIS,
                status=WorkflowStatus.PENDING,
                input_data={}
            )
        ]
        
        # 創建項目
        project = ProductProject(
            project_id=project_id,
            request=product_request,
            workflows=workflows,
            current_workflow=WorkflowType.DYNAMIC_MULTIMODAL_ANALYSIS
        )
        
        self.projects[project_id] = project
        
        logger.info(f"創建Personal產品項目: {project_id}")
        return project_id
    
    async def execute_product_development(self, project_id: str) -> ProductProject:
        """執行Personal產品開發流程"""
        if project_id not in self.projects:
            raise ValueError(f"項目不存在: {project_id}")
        
        project = self.projects[project_id]
        project.overall_status = WorkflowStatus.RUNNING
        
        logger.info(f"開始執行Personal產品開發: {project_id}")
        
        try:
            # 執行動態多模態分析
            multimodal_task = project.workflows[0]
            project.current_workflow = WorkflowType.DYNAMIC_MULTIMODAL_ANALYSIS
            
            multimodal_task = await self.engines[WorkflowType.DYNAMIC_MULTIMODAL_ANALYSIS].execute(multimodal_task)
            project.progress = 50.0
            
            if multimodal_task.status == WorkflowStatus.COMPLETED:
                # 執行多模態需求分析
                requirement_task = project.workflows[1]
                project.current_workflow = WorkflowType.MULTIMODAL_REQUIREMENT_ANALYSIS
                
                # 將第一階段結果作為第二階段輸入
                requirement_task.input_data.update({
                    "description": project.request.description,
                    "context": project.request.requirements,
                    "multimodal_analysis": multimodal_task.output_data.get("multimodal_analysis", {})
                })
                
                requirement_task = await self.engines[WorkflowType.MULTIMODAL_REQUIREMENT_ANALYSIS].execute(requirement_task)
                project.progress = 100.0
                
                if requirement_task.status == WorkflowStatus.COMPLETED:
                    project.overall_status = WorkflowStatus.COMPLETED
                    
                    # 整合結果
                    project.artifacts = {
                        "multimodal_analysis": multimodal_task.output_data,
                        "requirement_analysis": requirement_task.output_data,
                        "final_recommendations": self._generate_final_recommendations(
                            multimodal_task.output_data,
                            requirement_task.output_data
                        )
                    }
                else:
                    project.overall_status = WorkflowStatus.FAILED
            else:
                project.overall_status = WorkflowStatus.FAILED
                
        except Exception as e:
            project.overall_status = WorkflowStatus.FAILED
            logger.error(f"Personal產品開發執行失敗: {e}")
        
        logger.info(f"Personal產品開發完成: {project_id}, 狀態: {project.overall_status}")
        return project
    
    def _generate_final_recommendations(self, multimodal_result: Dict, requirement_result: Dict) -> Dict:
        """生成最終建議"""
        return {
            "integrated_analysis": {
                "multimodal_insights": multimodal_result.get("dynamic_insights", []),
                "technical_requirements": requirement_result.get("technical_requirements", {}),
                "technology_stack": requirement_result.get("technology_recommendations", [])
            },
            "development_roadmap": {
                "phase_1": "需求確認和技術選型",
                "phase_2": "架構設計和原型開發", 
                "phase_3": "功能實現和測試",
                "phase_4": "部署和運維"
            },
            "confidence_metrics": {
                "multimodal_confidence": multimodal_result.get("confidence_score", 0),
                "requirement_confidence": requirement_result.get("complexity_score", 0),
                "overall_confidence": (
                    multimodal_result.get("confidence_score", 0) + 
                    requirement_result.get("complexity_score", 0)
                ) / 2
            }
        }
    
    def get_project_status(self, project_id: str) -> Dict[str, Any]:
        """獲取項目狀態"""
        if project_id not in self.projects:
            return {"error": "項目不存在"}
        
        project = self.projects[project_id]
        return {
            "project_id": project_id,
            "status": project.overall_status.value,
            "progress": project.progress,
            "current_workflow": project.current_workflow.value if project.current_workflow else None,
            "workflows": [
                {
                    "type": task.workflow_type.value,
                    "status": task.status.value,
                    "started_at": task.started_at,
                    "completed_at": task.completed_at
                }
                for task in project.workflows
            ]
        }

# ============================================================================
# 4. Flask API服務
# ============================================================================

app = Flask(__name__)
CORS(app)

# 全局編排器實例
orchestrator = PersonalProductOrchestrator()

@app.route('/api/create_product', methods=['POST'])
async def create_product():
    """創建產品開發項目API"""
    try:
        data = request.get_json()
        
        product_request = ProductRequest(
            request_id=str(uuid.uuid4()),
            user_id=data.get('user_id', 'personal_user'),
            product_name=data.get('product_name', ''),
            product_type=ProductType(data.get('product_type', 'web_application')),
            description=data.get('description', ''),
            requirements=data.get('requirements', {}),
            priority=data.get('priority', 'normal')
        )
        
        project_id = await orchestrator.create_product(product_request)
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "message": "Personal產品項目創建成功"
        })
        
    except Exception as e:
        logger.error(f"創建產品項目失敗: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/execute_development/<project_id>', methods=['POST'])
async def execute_development(project_id: str):
    """執行產品開發API"""
    try:
        project = await orchestrator.execute_product_development(project_id)
        
        return jsonify({
            "success": True,
            "project": {
                "project_id": project.project_id,
                "status": project.overall_status.value,
                "progress": project.progress,
                "artifacts": project.artifacts
            }
        })
        
    except Exception as e:
        logger.error(f"執行產品開發失敗: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/project_status/<project_id>', methods=['GET'])
def get_project_status(project_id: str):
    """獲取項目狀態API"""
    try:
        status = orchestrator.get_project_status(project_id)
        return jsonify({
            "success": True,
            "status": status
        })
        
    except Exception as e:
        logger.error(f"獲取項目狀態失敗: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查API"""
    return jsonify({
        "success": True,
        "service": "Personal Product Orchestrator",
        "version": "1.0.0",
        "engines": list(orchestrator.engines.keys()),
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    import sys
    port = 5003
    if len(sys.argv) > 1 and sys.argv[1] == '--port':
        port = int(sys.argv[2])
    
    logger.info("啟動Personal Product Orchestrator服務...")
    app.run(host="0.0.0.0", port=port, debug=True)

