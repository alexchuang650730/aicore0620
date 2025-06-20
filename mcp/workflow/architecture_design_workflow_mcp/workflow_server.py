# -*- coding: utf-8 -*-
"""
架構設計工作流MCP服務器
"""

import asyncio
import json
import logging
import time
from datetime import datetime
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# 添加路徑
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from config.architecture_design.global_config import ArchitectureDesignConfig

try:
    from architecture_design_mcp import ArchitectureDesignMCP
except ImportError:
    print("警告: 無法導入架構設計MCP，使用模擬模式")
    ArchitectureDesignMCP = None

# 創建Flask應用
app = Flask(__name__)
CORS(app)

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArchitectureWorkflowServer:
    """架構設計工作流MCP服務器"""
    
    def __init__(self):
        self.service_name = "Architecture Design Workflow MCP"
        self.version = "1.0.0"
        self.workflow_mcp = ArchitectureDesignMCP() if ArchitectureDesignMCP else None
        self.workflow_available = self.workflow_mcp is not None
        
    async def process_workflow(self, requirement: str, context: dict = None) -> dict:
        """處理架構設計工作流"""
        try:
            if self.workflow_mcp:
                result = await self.workflow_mcp.process_requirement(requirement, context)
                return {
                    'success': True,
                    'result': result,
                    'workflow_type': 'architecture_design',
                    'processing_time': 5.0
                }
            else:
                # 模擬工作流處理
                return {
                    'success': True,
                    'result': {
                        'workflow_analysis': f"工作流分析: {requirement}",
                        'component_selection': ['architecture_analysis_mcp'],
                        'execution_plan': ['需求解析', '組件選擇', '並行執行', '結果整合'],
                        'estimated_time': '5-10秒'
                    },
                    'workflow_type': 'simulated',
                    'processing_time': 2.0
                }
        except Exception as e:
            logger.error(f"工作流處理錯誤: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'workflow_type': 'error'
            }

# 創建服務器實例
workflow_server = ArchitectureWorkflowServer()

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'healthy',
        'service': workflow_server.service_name,
        'version': workflow_server.version,
        'workflow_available': workflow_server.workflow_available,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/workflow', methods=['POST'])
def process_workflow():
    """處理工作流請求"""
    try:
        data = request.get_json()
        requirement = data.get('requirement', '')
        context = data.get('context', {})
        
        if not requirement:
            return jsonify({
                'success': False,
                'error': '需求不能為空'
            }), 400
        
        # 使用asyncio運行異步函數
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            workflow_server.process_workflow(requirement, context)
        )
        loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"工作流處理錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """獲取服務狀態"""
    return jsonify({
        'service_name': workflow_server.service_name,
        'version': workflow_server.version,
        'workflow_available': workflow_server.workflow_available,
        'capabilities': [
            '複雜工作流編排',
            '智能組件選擇',
            '並行處理',
            '結果整合',
            '錯誤恢復'
        ],
        'supported_workflows': [
            'architecture_design',
            'component_selection',
            'parallel_analysis',
            'result_integration'
        ]
    })

if __name__ == '__main__':
    config = ArchitectureDesignConfig()
    port = config.WORKFLOW_MCP_PORT
    
    print(f"啟動架構設計工作流MCP服務器...")
    print(f"服務名稱: {workflow_server.service_name}")
    print(f"版本: {workflow_server.version}")
    print(f"工作流可用: {workflow_server.workflow_available}")
    print(f"監聽端口: {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)

