#!/usr/bin/env python3
"""
需求分析MCP HTTP服務器
提供REST API接口來測試需求分析功能
"""

import asyncio
import json
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path

# 添加路徑
sys.path.append('/home/ubuntu/enterprise_deployment/aicore0619')

from mcp.adapter.requirement_analysis_mcp.requirement_analysis_mcp import RequirementAnalysisMcp

# 創建Flask應用
app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 初始化需求分析MCP
req_analysis_mcp = RequirementAnalysisMcp()

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查接口"""
    return jsonify({
        "status": "healthy",
        "service": "requirement_analysis_mcp",
        "version": "1.0.0"
    })

@app.route('/api/info', methods=['GET'])
def get_info():
    """獲取MCP信息"""
    return jsonify(req_analysis_mcp.get_info())

@app.route('/api/status', methods=['GET'])
async def get_status():
    """獲取MCP狀態"""
    status = await req_analysis_mcp.get_status()
    return jsonify(status)

@app.route('/api/analyze', methods=['POST'])
async def analyze_requirement():
    """分析需求接口"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "error": "No JSON data provided"
            }), 400
        
        # 設置請求類型為分析需求
        data["type"] = "analyze_requirement"
        
        result = await req_analysis_mcp.process(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/create', methods=['POST'])
async def create_requirement():
    """創建需求接口"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "error": "No JSON data provided"
            }), 400
        
        # 設置請求類型為創建需求
        data["type"] = "create_requirement"
        
        result = await req_analysis_mcp.process(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/validate', methods=['POST'])
async def validate_requirements():
    """驗證需求接口"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "error": "No JSON data provided"
            }), 400
        
        # 設置請求類型為驗證需求
        data["type"] = "validate_requirements"
        
        result = await req_analysis_mcp.process(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/estimate', methods=['POST'])
async def estimate_effort():
    """工作量估算接口"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "error": "No JSON data provided"
            }), 400
        
        # 設置請求類型為工作量估算
        data["type"] = "estimate_effort"
        
        result = await req_analysis_mcp.process(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/prioritize', methods=['POST'])
async def prioritize_requirements():
    """需求優先級排序接口"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "error": "No JSON data provided"
            }), 400
        
        # 設置請求類型為優先級排序
        data["type"] = "prioritize_requirements"
        
        result = await req_analysis_mcp.process(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/document', methods=['POST'])
async def generate_documentation():
    """生成需求文檔接口"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "error": "No JSON data provided"
            }), 400
        
        # 設置請求類型為生成文檔
        data["type"] = "generate_documentation"
        
        result = await req_analysis_mcp.process(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/session/start', methods=['POST'])
async def start_analysis_session():
    """開始分析會話接口"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "error": "No JSON data provided"
            }), 400
        
        # 設置請求類型為開始分析會話
        data["type"] = "start_analysis_session"
        
        result = await req_analysis_mcp.process(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/session/status', methods=['GET'])
async def get_analysis_status():
    """獲取分析狀態接口"""
    try:
        session_id = request.args.get('session_id')
        if not session_id:
            return jsonify({
                "status": "error",
                "error": "session_id parameter required"
            }), 400
        
        data = {
            "type": "get_analysis_status",
            "session_id": session_id
        }
        
        result = await req_analysis_mcp.process(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

# 測試接口
@app.route('/api/test/snake-game', methods=['POST'])
async def test_snake_game_analysis():
    """測試貪吃蛇遊戲需求分析"""
    try:
        # 預定義的貪吃蛇遊戲需求
        snake_game_data = {
            "type": "analyze_requirement",
            "requirement": "開發一個Python貪吃蛇遊戲，包含遊戲邏輯、圖形界面和計分系統",
            "requirement_type": "functional",
            "project_context": {
                "name": "貪吃蛇遊戲",
                "technology": "Python + pygame",
                "target_users": "遊戲玩家",
                "complexity": "medium"
            }
        }
        
        result = await req_analysis_mcp.process(snake_game_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 啟動需求分析MCP HTTP服務器...")
    print("📋 可用的API接口:")
    print("  GET  /health - 健康檢查")
    print("  GET  /api/info - 獲取MCP信息")
    print("  GET  /api/status - 獲取MCP狀態")
    print("  POST /api/analyze - 分析需求")
    print("  POST /api/create - 創建需求")
    print("  POST /api/validate - 驗證需求")
    print("  POST /api/estimate - 工作量估算")
    print("  POST /api/prioritize - 需求優先級排序")
    print("  POST /api/document - 生成需求文檔")
    print("  POST /api/session/start - 開始分析會話")
    print("  GET  /api/session/status - 獲取分析狀態")
    print("  POST /api/test/snake-game - 測試貪吃蛇遊戲需求分析")
    print("\n🌐 服務器地址: http://localhost:8100")
    
    app.run(host='0.0.0.0', port=8100, debug=True)

