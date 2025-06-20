#!/usr/bin/env python3
"""
多模態需求分析HTTP服務
整合現有的MCP組件和產品編排系統
"""

import asyncio
import json
import uuid
import logging
import os
import tempfile
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import werkzeug
from werkzeug.utils import secure_filename

# 導入現有組件
import sys
sys.path.append('/tmp/aicore0619')
sys.path.append('/home/ubuntu/enterprise_deployment')

from interactive_requirement_analysis_workflow_mcp import InteractiveRequirementAnalysisWorkflowMCP
from mcp.coordinator.workflow_collaboration.product_orchestrator_v3 import ProductOrchestratorV3
from multimodal_document_processor import MultimodalDocumentProcessor
from incremental_engine import IncrementalEngine

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 創建Flask應用
app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 全局組件實例
workflow_mcp = None
orchestrator = None
document_processor = None
incremental_engine = None
active_sessions = {}
analysis_versions = {}  # 存儲分析版本

# 支持的文件類型
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', 'csv', 'xls', 'xlsx', 'md', 'py', 'js', 'html', 'css', 'json', 'xml'}

def allowed_file(filename):
    """檢查文件類型是否支持"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_components():
    """初始化MCP組件"""
    global workflow_mcp, orchestrator, document_processor
    
    try:
        # 初始化多模態文檔處理器
        document_processor = MultimodalDocumentProcessor()
        logger.info("✅ MultimodalDocumentProcessor 初始化成功")
        
        # 初始化互動式需求分析工作流MCP
        workflow_mcp = InteractiveRequirementAnalysisWorkflowMCP()
        logger.info("✅ InteractiveRequirementAnalysisWorkflowMCP 初始化成功")
        
        # 初始化產品編排器
        orchestrator = ProductOrchestratorV3()
        logger.info("✅ ProductOrchestratorV3 初始化成功")
        
        return True
    except Exception as e:
        logger.error(f"❌ 組件初始化失敗: {e}")
        return False
@app.route('/')
def home():
    """根路徑歡迎頁面"""
    return """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>多模態需求分析系統</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }
            .code { background: #f1f1f1; padding: 10px; font-family: monospace; border-radius: 3px; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 10px 0; }
            a { color: #007bff; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 多模態需求分析系統</h1>
            
            <div class="status">
                ✅ 系統運行正常 - 所有組件已初始化
            </div>
            
            <h2>📋 系統功能</h2>
            <ul>
                <li>🔄 互動式需求分析</li>
                <li>📄 多模態文檔處理</li>
                <li>❓ 主動提問和澄清</li>
                <li>🎯 產品編排整合</li>
                <li>💬 多輪對話支持</li>
            </ul>
            
            <h2>🌐 API端點</h2>
            
            <div class="endpoint">
                <strong>健康檢查</strong><br>
                <a href="/health" target="_blank">GET /health</a>
            </div>
            
            <div class="endpoint">
                <strong>API信息</strong><br>
                <a href="/api/info" target="_blank">GET /api/info</a>
            </div>
            
            <div class="endpoint">
                <strong>開始分析會話</strong><br>
                POST /api/start-session
            </div>
            
            <div class="endpoint">
                <strong>上傳文檔分析</strong><br>
                POST /api/upload-document
            </div>
            
            <h2>🧪 測試示例</h2>
            
            <h3>開始需求分析</h3>
            <div class="code">
curl -X POST /api/start-session \\<br>
&nbsp;&nbsp;-H "Content-Type: application/json" \\<br>
&nbsp;&nbsp;-d '{"requirement": "我想開發一個電商網站"}'
            </div>
            
            <h3>上傳文檔</h3>
            <div class="code">
curl -X POST /api/upload-document \\<br>
&nbsp;&nbsp;-F "file=@document.pdf"
            </div>
            
            <h2>📊 支持格式</h2>
            <p>支持21種文件格式：PDF, DOC, DOCX, TXT, PNG, JPG, CSV, XLS, XLSX, MD, PY, JS, HTML, CSS, JSON, XML等</p>
            
            <div style="text-align: center; margin-top: 30px; color: #666;">
                <p>Powered by Manus AI | Version 1.0.0</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/health'), methods=['GET'])
def health_check():
    """健康檢查"""
    return jsonify({
        "status": "healthy",
        "service": "多模態需求分析服務",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "workflow_mcp": workflow_mcp is not None,
            "orchestrator": orchestrator is not None,
            "document_processor": document_processor is not None
        }
    })

@app.route('/api/info', methods=['GET'])
def get_service_info():
    """獲取服務信息"""
    return jsonify({
        "service_name": "多模態需求分析HTTP服務",
        "version": "1.0.0",
        "description": "整合MCP組件和產品編排系統的需求分析服務",
        "features": [
            "互動式需求分析",
            "多模態文檔處理",
            "主動提問和澄清",
            "產品編排整合",
            "多輪對話支持"
        ],
        "supported_formats": list(ALLOWED_EXTENSIONS),
        "endpoints": [
            "/api/start-session - 開始新的需求分析會話",
            "/api/analyze-text - 分析文本需求",
            "/api/upload-document - 上傳文檔進行分析",
            "/api/answer-question - 回答系統問題",
            "/api/get-session - 獲取會話狀態",
            "/api/orchestrate - 使用產品編排器處理需求"
        ]
    })

@app.route('/api/start-session', methods=['POST'])
def start_analysis_session():
    """開始新的需求分析會話"""
    try:
        data = request.get_json()
        initial_requirement = data.get('requirement', '')
        
        if not initial_requirement:
            return jsonify({"error": "需求描述不能為空"}), 400
        
        # 創建新會話
        session_id = str(uuid.uuid4())
        
        # 使用工作流MCP開始分析
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            session = loop.run_until_complete(
                workflow_mcp.start_analysis_session(initial_requirement)
            )
            
            active_sessions[session_id] = session
            
            return jsonify({
                "success": True,
                "session_id": session_id,
                "initial_analysis": {
                    "confidence_level": session.confidence_level,
                    "pending_questions": [
                        {
                            "question_id": q.question_id,
                            "type": q.question_type.value,
                            "urgency": q.urgency.value,
                            "question": q.question_text,
                            "context": q.context,
                            "suggested_answers": q.suggested_answers
                        }
                        for q in session.pending_questions
                    ],
                    "completed_aspects": session.completed_aspects,
                    "next_action": session.next_recommended_action
                }
            })
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"開始會話失敗: {e}")
        return jsonify({"error": f"開始會話失敗: {str(e)}"}), 500

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text_requirement():
    """分析文本需求"""
    try:
        data = request.get_json()
        requirement_text = data.get('text', '')
        session_id = data.get('session_id')
        
        if not requirement_text:
            return jsonify({"error": "需求文本不能為空"}), 400
        
        # 如果有會話ID，使用現有會話；否則創建新會話
        if session_id and session_id in active_sessions:
            session = active_sessions[session_id]
        else:
            # 創建新會話
            session_id = str(uuid.uuid4())
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                session = loop.run_until_complete(
                    workflow_mcp.start_analysis_session(requirement_text)
                )
                active_sessions[session_id] = session
            finally:
                loop.close()
        
        # 執行分析
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            analysis_result = loop.run_until_complete(
                workflow_mcp.analyze_requirement_interactive(session_id, requirement_text)
            )
            
            return jsonify({
                "success": True,
                "session_id": session_id,
                "analysis": analysis_result
            })
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"文本分析失敗: {e}")
        return jsonify({"error": f"文本分析失敗: {str(e)}"}), 500

@app.route('/api/upload-document', methods=['POST'])
def upload_and_analyze_document():
    """上傳文檔並進行分析"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "沒有上傳文件"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "沒有選擇文件"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": f"不支持的文件類型，支持的類型: {ALLOWED_EXTENSIONS}"}), 400
        
        # 保存上傳的文件
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, filename)
        file.save(file_path)
        
        session_id = request.form.get('session_id', str(uuid.uuid4()))
        
        # 使用多模態文檔處理器處理文檔
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            processing_result = loop.run_until_complete(
                document_processor.process_document(file_path, filename)
            )
            
            if not processing_result.get("success", False):
                return jsonify({
                    "success": False,
                    "error": processing_result.get("error", "文檔處理失敗")
                }), 500
            
            # 將處理結果整合到需求分析中
            if session_id not in active_sessions:
                # 創建新會話，使用文檔內容作為初始需求
                initial_requirement = f"文檔分析: {filename}"
                if processing_result.get("content"):
                    initial_requirement += f"\\n\\n內容摘要: {processing_result['content'][:500]}..."
                
                session = loop.run_until_complete(
                    workflow_mcp.start_analysis_session(initial_requirement)
                )
                active_sessions[session_id] = session
            
            # 使用工作流MCP分析文檔內容
            analysis_result = loop.run_until_complete(
                workflow_mcp.analyze_document_content(session_id, processing_result)
            )
            
            return jsonify({
                "success": True,
                "session_id": session_id,
                "filename": filename,
                "document_processing": processing_result,
                "analysis": analysis_result
            })
        finally:
            loop.close()
            # 清理臨時文件
            os.remove(file_path)
            os.rmdir(temp_dir)
            
    except Exception as e:
        logger.error(f"文檔分析失敗: {e}")
        return jsonify({"error": f"文檔分析失敗: {str(e)}"}), 500

@app.route('/api/answer-question', methods=['POST'])
def answer_question():
    """回答系統提出的問題"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        question_id = data.get('question_id')
        answer = data.get('answer')
        
        if not all([session_id, question_id, answer]):
            return jsonify({"error": "缺少必要參數"}), 400
        
        if session_id not in active_sessions:
            return jsonify({"error": "會話不存在"}), 404
        
        # 處理用戶回答
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                workflow_mcp.process_user_answer(session_id, question_id, answer)
            )
            
            return jsonify({
                "success": True,
                "result": result
            })
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"處理回答失敗: {e}")
        return jsonify({"error": f"處理回答失敗: {str(e)}"}), 500

@app.route('/api/get-session', methods=['GET'])
def get_session_status():
    """獲取會話狀態"""
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return jsonify({"error": "缺少session_id參數"}), 400
        
        if session_id not in active_sessions:
            return jsonify({"error": "會話不存在"}), 404
        
        session = active_sessions[session_id]
        
        return jsonify({
            "success": True,
            "session": {
                "session_id": session.session_id,
                "initial_requirement": session.initial_requirement,
                "confidence_level": session.confidence_level,
                "completed_aspects": session.completed_aspects,
                "pending_questions": [
                    {
                        "question_id": q.question_id,
                        "type": q.question_type.value,
                        "urgency": q.urgency.value,
                        "question": q.question_text,
                        "context": q.context,
                        "suggested_answers": q.suggested_answers
                    }
                    for q in session.pending_questions
                ],
                "conversation_history": [
                    {
                        "turn_id": turn.turn_id,
                        "timestamp": turn.timestamp.isoformat(),
                        "speaker": turn.speaker,
                        "content": turn.content,
                        "analysis_progress": turn.analysis_progress
                    }
                    for turn in session.conversation_history
                ],
                "next_action": session.next_recommended_action
            }
        })
        
    except Exception as e:
        logger.error(f"獲取會話狀態失敗: {e}")
        return jsonify({"error": f"獲取會話狀態失敗: {str(e)}"}), 500

@app.route('/api/orchestrate', methods=['POST'])
def orchestrate_requirement():
    """使用產品編排器處理需求"""
    try:
        data = request.get_json()
        requirements = data.get('requirements')
        
        if not requirements:
            return jsonify({"error": "需求信息不能為空"}), 400
        
        # 使用產品編排器
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                orchestrator.create_and_execute_workflow(requirements)
            )
            
            return jsonify({
                "success": True,
                "orchestration_result": result
            })
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"產品編排失敗: {e}")
        return jsonify({"error": f"產品編排失敗: {str(e)}"}), 500

@app.route('/api/sessions', methods=['GET'])
def list_active_sessions():
    """列出所有活躍會話"""
    try:
        sessions_info = []
        for session_id, session in active_sessions.items():
            sessions_info.append({
                "session_id": session_id,
                "initial_requirement": session.initial_requirement[:100] + "..." if len(session.initial_requirement) > 100 else session.initial_requirement,
                "confidence_level": session.confidence_level,
                "pending_questions_count": len(session.pending_questions),
                "completed_aspects_count": len(session.completed_aspects)
            })
        
        return jsonify({
            "success": True,
            "active_sessions_count": len(active_sessions),
            "sessions": sessions_info
        })
        
    except Exception as e:
        logger.error(f"列出會話失敗: {e}")
        return jsonify({"error": f"列出會話失敗: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 啟動多模態需求分析HTTP服務...")
    
    # 初始化組件
    if init_components():
        print("✅ 所有組件初始化成功")
        print("🌐 服務地址: http://0.0.0.0:8300")
        print("📋 API文檔: http://0.0.0.0:8300/api/info")
        print("💊 健康檢查: http://0.0.0.0:8300/health")
        
        # 啟動服務
        app.run(host='0.0.0.0', port=8300, debug=False)
    else:
        print("❌ 組件初始化失敗，無法啟動服務")

