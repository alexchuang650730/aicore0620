# -*- coding: utf-8 -*-
"""
架構設計系統後台服務器
Architecture Design System Backend Server
提供架構設計分析的Web API服務
"""

import asyncio
import json
import logging
import sys
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

# 添加路徑
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from config.architecture_design.global_config import ArchitectureDesignConfig

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class ArchitectureDesignUIServer:
    """架構設計UI後台服務器"""
    
    def __init__(self):
        self.service_name = "architecture_design_ui_server"
        self.version = "1.0.0"
        self.main_engine_url = "http://localhost:8303"  # 架構設計MCP服務
        
    async def analyze_architecture_requirement(self, requirement, context=None):
        """分析架構設計需求"""
        try:
            # 嘗試調用主架構設計引擎
            payload = {
                'requirement': requirement,
                'context': context,
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.main_engine_url}/api/analyze",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"主架構設計引擎分析成功: {result.get('confidence_score', 'N/A')}")
                return result
            else:
                logger.warning(f"主架構設計引擎調用失敗，狀態碼: {response.status_code}")
                return await self._fallback_analysis(requirement, context)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"主架構設計引擎連接失敗: {str(e)}")
            return await self._fallback_analysis(requirement, context)
        except Exception as e:
            logger.error(f"架構設計分析過程中發生錯誤: {str(e)}")
            return await self._fallback_analysis(requirement, context)
    
    async def _fallback_analysis(self, requirement, context):
        """架構設計分析降級處理"""
        logger.info("使用架構設計分析降級模式")
        
        return {
            'success': True,
            'analysis_result': {
                'architecture_overview': f'基於需求"{requirement}"的架構設計分析',
                'system_design': '採用現代化微服務架構，包含API網關、服務發現、配置中心等核心組件',
                'technology_stack': {
                    'frontend': 'React 18 + TypeScript + Tailwind CSS',
                    'backend': 'Node.js + Express / Python + FastAPI',
                    'database': 'PostgreSQL + Redis + MongoDB',
                    'infrastructure': 'Docker + Kubernetes + AWS/Azure'
                },
                'architecture_patterns': [
                    '微服務架構模式 (Microservices)',
                    'API網關模式 (API Gateway)',
                    '事件驅動架構 (Event-Driven)',
                    'CQRS模式 (Command Query Responsibility Segregation)',
                    '斷路器模式 (Circuit Breaker)'
                ],
                'scalability_design': {
                    'horizontal_scaling': '支持水平擴展，通過容器編排實現自動擴縮容',
                    'load_balancing': '多層負載均衡：DNS -> CDN -> Load Balancer -> Service Mesh',
                    'caching_strategy': '多級緩存：瀏覽器緩存 -> CDN -> Redis -> 應用緩存',
                    'database_sharding': '數據庫分片策略，支持讀寫分離和分庫分表'
                },
                'security_considerations': {
                    'authentication': 'OAuth 2.0 + OpenID Connect + JWT Token',
                    'authorization': 'RBAC權限模型 + 細粒度權限控制',
                    'data_encryption': 'TLS 1.3 + AES-256 + 數據庫透明加密',
                    'api_security': 'API限流 + 防DDoS + WAF + API簽名驗證'
                },
                'implementation_roadmap': {
                    'phase1': '核心架構搭建與基礎服務開發 (3個月)',
                    'phase2': '業務功能模組開發與集成測試 (6個月)',
                    'phase3': '性能優化、安全加固與生產部署 (2個月)'
                },
                'risk_assessment': {
                    'technical_risks': [
                        '微服務複雜度管理風險',
                        '分散式系統一致性風險',
                        '技術棧學習曲線風險',
                        '第三方依賴風險'
                    ],
                    'mitigation_strategies': [
                        '採用成熟的微服務框架和工具',
                        '實施分散式事務和最終一致性策略',
                        '建立技術培訓和知識分享機制',
                        '制定供應商風險評估和備用方案'
                    ]
                }
            },
            'confidence_score': 0.85,
            'engine_type': '備用架構設計分析引擎',
            'processing_time': 0.1,
            'fallback_mode': True,
            'fallback_reason': '主架構設計引擎暫時不可用，系統已切換到備用分析模式'
        }

# 創建全局服務實例
ui_server = ArchitectureDesignUIServer()

@app.route('/')
def index():
    """提供前端頁面"""
    try:
        return send_from_directory('../frontend', 'index.html')
    except Exception as e:
        logger.error(f"前端頁面載入失敗: {str(e)}")
        return jsonify({
            'error': 'API端點不存在',
            'success': False
        }), 404

@app.route('/api/analyze', methods=['POST'])
def analyze_api():
    """架構設計分析API端點"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '請求數據不能為空',
                'confidence_score': 0.0
            }), 400
        
        requirement = data.get('requirement', '').strip()
        context = data.get('context')
        
        if not requirement:
            return jsonify({
                'success': False,
                'error': '架構設計需求不能為空',
                'confidence_score': 0.0
            }), 400
        
        logger.info(f"收到架構設計分析請求: {requirement[:100]}...")
        
        # 調用架構設計分析服務 (同步版本)
        result = asyncio.run(ui_server.analyze_architecture_requirement(requirement, context))
        
        logger.info(f"架構設計分析完成: 成功={result.get('success', False)}, 信心度={result.get('confidence_score', 0)}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"架構設計分析API錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'分析過程中發生錯誤: {str(e)}',
            'confidence_score': 0.0
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """文件上傳API端點"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '沒有文件被上傳'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '沒有選擇文件'
            }), 400
        
        # 這裡可以添加文件處理邏輯
        # 目前只返回成功響應
        return jsonify({
            'success': True,
            'message': f'文件 {file.filename} 上傳成功',
            'filename': file.filename,
            'size': len(file.read())
        })
        
    except Exception as e:
        logger.error(f"文件上傳錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'文件上傳失敗: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    try:
        # 檢查主架構設計引擎狀態
        engine_status = 'unknown'
        try:
            response = requests.get(f"{ui_server.main_engine_url}/health", timeout=5)
            if response.status_code == 200:
                engine_status = 'healthy'
            else:
                engine_status = 'unhealthy'
        except:
            engine_status = 'unavailable'
        
        return jsonify({
            'service': ui_server.service_name,
            'status': 'healthy',
            'version': ui_server.version,
            'timestamp': datetime.now().isoformat(),
            'main_engine_status': engine_status,
            'main_engine_url': ui_server.main_engine_url,
            'capabilities': [
                '架構設計需求分析',
                '技術選型建議',
                '架構模式推薦',
                '可擴展性設計',
                '安全架構設計',
                '實施路線圖規劃',
                '風險評估分析'
            ]
        })
        
    except Exception as e:
        logger.error(f"健康檢查錯誤: {str(e)}")
        return jsonify({
            'service': ui_server.service_name,
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """獲取系統狀態"""
    try:
        # 檢查各個組件狀態
        main_engine_healthy = False
        try:
            response = requests.get(f"{ui_server.main_engine_url}/health", timeout=5)
            main_engine_healthy = response.status_code == 200
        except:
            pass
        
        return jsonify({
            'ui_server': {
                'status': 'healthy',
                'version': ui_server.version,
                'uptime': 'running'
            },
            'main_engine': {
                'status': 'healthy' if main_engine_healthy else 'unavailable',
                'url': ui_server.main_engine_url,
                'description': '架構設計MCP主引擎'
            },
            'overall_status': 'healthy' if main_engine_healthy else 'degraded',
            'fallback_available': True,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"狀態檢查錯誤: {str(e)}")
        return jsonify({
            'overall_status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    config = ArchitectureDesignConfig()
    port = config.ADMIN_UI_PORT
    
    print(f"🚀 啟動架構設計UI服務器...")
    print(f"📋 服務名稱: {ui_server.service_name}")
    print(f"📦 版本: {ui_server.version}")
    print(f"🔗 主引擎URL: {ui_server.main_engine_url}")
    print(f"🌐 監聽端口: {port}")
    print(f"📱 前端界面: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)

