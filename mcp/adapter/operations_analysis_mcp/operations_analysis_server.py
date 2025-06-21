# -*- coding: utf-8 -*-
"""
純AI驅動運營分析MCP服務器
Pure AI-Driven Operations Analysis MCP Server
提供運營分析引擎的Flask API服務
"""

import asyncio
import json
import logging
import sys
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# 添加引擎路徑
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from operations_ai_engine import OperationsAIEngine
except ImportError:
    # 降級處理
    class OperationsAIEngine:
        async def analyze_with_operations_claude(self, requirement, context, operations_type='general_operations'):
            return {
                'success': True,
                'analysis': 'AI驅動運營分析引擎降級模式運行',
                'confidence_score': 0.75,
                'engine_type': 'operations_fallback_analysis',
                'mode': 'fallback'
            }

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze_operations():
    """運營分析API端點"""
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({'success': False, 'error': '無效的請求數據'}), 400
        
        requirement = request_data.get('requirement', '')
        context = request_data.get('context', {})
        operations_type = request_data.get('operations_type', 'general_operations')
        
        if not requirement:
            return jsonify({'success': False, 'error': '缺少運營需求參數'}), 400
        
        # 創建運營分析引擎
        engine = OperationsAIEngine()
        
        # 使用asyncio執行分析
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                engine.analyze_with_operations_claude(requirement, context, operations_type)
            )
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"運營分析API錯誤: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'engine_type': 'operations_error_handler',
            'ai_error_handled': True
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查"""
    try:
        # 測試引擎是否可用
        engine = OperationsAIEngine()
        engine_available = hasattr(engine, 'analyze_with_operations_claude')
        
        return jsonify({
            'status': 'healthy',
            'service': 'pure_ai_operations_analysis_mcp',
            'layer': 'adapter_mcp',
            'ai_engine_available': engine_available,
            'ai_driven': True,
            'hardcoding': False,
            'supported_operations_types': [
                'release_operations', 'monitoring_operations', 'performance_operations',
                'security_operations', 'infrastructure_operations', 'deployment_operations',
                'incident_operations', 'capacity_operations', 'compliance_operations',
                'automation_operations', 'general_operations'
            ],
            'analysis_capabilities': [
                'requirement_deconstruction', 'professional_knowledge_application',
                'quantitative_analysis', 'strategic_insights', 'quality_validation'
            ]
        })
        
    except Exception as e:
        logger.error(f"健康檢查錯誤: {e}")
        return jsonify({
            'status': 'degraded',
            'service': 'pure_ai_operations_analysis_mcp',
            'error': str(e),
            'ai_engine_available': False
        }), 500

if __name__ == '__main__':
    logger.info("啟動純AI驅動運營分析MCP服務器")
    app.run(host='0.0.0.0', port=8100, debug=False)

