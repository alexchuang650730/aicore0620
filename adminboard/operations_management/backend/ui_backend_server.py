# -*- coding: utf-8 -*-
"""
運營管理中心後端API服務
Operations Management Center Backend API Service
專門為運營管理中心提供實時監控和管理功能的後台服務
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import time
import logging
import psutil
import sqlite3
from datetime import datetime, timedelta
import requests
import threading
from typing import Dict, List, Any

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 配置
DATABASE_FILE = 'operations_management.db'
ALERT_THRESHOLD_CPU = 80.0
ALERT_THRESHOLD_MEMORY = 90.0
ALERT_THRESHOLD_DISK = 85.0

# 監控的服務配置 (修正測試組件服務配置)
MONITORED_SERVICES = {
    "需求分析服務": {
        "url": "http://localhost:5000/health",
        "port": 5000,
        "description": "需求分析UI後端服務"
    },
    "發布管理服務": {
        "url": "http://localhost:5002/health", 
        "port": 5002,
        "description": "發布管理UI後端服務"
    },
    "測試管理工作流MCP": {
        "url": "http://localhost:8321/health",
        "port": 8321,
        "description": "純AI驅動測試管理工作流MCP服務"
    },
    "AI分析引擎": {
        "url": "http://localhost:8888/health",
        "port": 8888,
        "description": "純AI驅動需求分析引擎"
    },
    "運營工作流MCP": {
        "url": "http://localhost:8091/health",
        "port": 8091,
        "description": "純AI驅動運營工作流MCP服務"
    },
    "運營分析引擎": {
        "url": "http://localhost:8100/health",
        "port": 8100,
        "description": "純AI驅動運營分析引擎"
    }
}

class OperationsManager:
    """運營管理核心類"""
    
    def __init__(self):
        self.init_database()
        self.start_monitoring()
    
    def init_database(self):
        """初始化數據庫"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # 創建告警表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                type TEXT NOT NULL,
                message TEXT NOT NULL,
                severity TEXT NOT NULL,
                resolved BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # 創建服務狀態表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS service_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_name TEXT NOT NULL,
                status TEXT NOT NULL,
                response_time REAL,
                timestamp TEXT NOT NULL,
                details TEXT
            )
        ''')
        
        # 創建系統資源表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL,
                network_io TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def start_monitoring(self):
        """啟動監控線程"""
        def monitor_loop():
            while True:
                try:
                    self.check_system_resources()
                    self.check_services()
                    time.sleep(30)  # 每30秒檢查一次
                except Exception as e:
                    logger.error(f"監控循環錯誤: {e}")
                    time.sleep(60)  # 錯誤時等待1分鐘
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        logger.info("監控線程已啟動")
    
    def check_system_resources(self):
        """檢查系統資源"""
        try:
            # 獲取系統資源使用情況
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # 記錄到數據庫
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO system_resources 
                (timestamp, cpu_percent, memory_percent, disk_percent)
                VALUES (?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                cpu_percent,
                memory.percent,
                disk.percent
            ))
            
            # 檢查是否需要告警
            if cpu_percent > ALERT_THRESHOLD_CPU:
                self.create_alert('system', f'CPU使用率過高: {cpu_percent:.1f}%', 'warning')
            
            if memory.percent > ALERT_THRESHOLD_MEMORY:
                self.create_alert('system', f'記憶體使用率過高: {memory.percent:.1f}%', 'critical')
            
            if disk.percent > ALERT_THRESHOLD_DISK:
                self.create_alert('system', f'磁碟使用率過高: {disk.percent:.1f}%', 'warning')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"檢查系統資源失敗: {e}")
    
    def check_services(self):
        """檢查服務狀態"""
        for service_name, config in MONITORED_SERVICES.items():
            try:
                start_time = time.time()
                response = requests.get(config['url'], timeout=5)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    status = 'running'
                    details = response.json() if response.headers.get('content-type', '').startswith('application/json') else None
                else:
                    status = 'error'
                    details = {'error': f'HTTP {response.status_code}'}
                    self.create_alert('service', f'{service_name} 返回錯誤狀態碼: {response.status_code}', 'warning')
                
            except requests.exceptions.ConnectionError:
                status = 'error'
                response_time = None
                details = {'error': '連接被拒絕'}
                self.create_alert('service', f'{service_name} 連接被拒絕', 'critical')
                
            except requests.exceptions.Timeout:
                status = 'warning'
                response_time = None
                details = {'error': '請求超時'}
                self.create_alert('service', f'{service_name} 請求超時', 'warning')
                
            except Exception as e:
                status = 'error'
                response_time = None
                details = {'error': str(e)}
                self.create_alert('service', f'{service_name} 檢查失敗: {str(e)}', 'warning')
            
            # 記錄服務狀態
            self.record_service_status(service_name, status, response_time, details)
    
    def record_service_status(self, service_name: str, status: str, response_time: float = None, details: Dict = None):
        """記錄服務狀態"""
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO service_status 
                (service_name, status, response_time, timestamp, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                service_name,
                status,
                response_time,
                datetime.now().isoformat(),
                json.dumps(details) if details else None
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"記錄服務狀態失敗: {e}")
    
    def create_alert(self, alert_type: str, message: str, severity: str):
        """創建告警"""
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            
            # 檢查是否已有相同的未解決告警
            cursor.execute('''
                SELECT id FROM alerts 
                WHERE type = ? AND message = ? AND resolved = FALSE
            ''', (alert_type, message))
            
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO alerts (timestamp, type, message, severity)
                    VALUES (?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    alert_type,
                    message,
                    severity
                ))
                
                conn.commit()
                logger.info(f"創建告警: {message}")
            
            conn.close()
            
        except Exception as e:
            logger.error(f"創建告警失敗: {e}")
    
    def get_system_overview(self) -> Dict[str, Any]:
        """獲取系統概覽"""
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            
            # 獲取活動告警數量
            cursor.execute('SELECT COUNT(*) FROM alerts WHERE resolved = FALSE')
            active_alerts = cursor.fetchone()[0]
            
            # 獲取服務狀態統計
            cursor.execute('''
                SELECT status, COUNT(*) FROM (
                    SELECT service_name, status FROM service_status 
                    WHERE id IN (
                        SELECT MAX(id) FROM service_status 
                        GROUP BY service_name
                    )
                ) GROUP BY status
            ''')
            
            service_stats = dict(cursor.fetchall())
            total_services = len(MONITORED_SERVICES)
            active_services = service_stats.get('running', 0)
            
            conn.close()
            
            return {
                'status': 'healthy' if active_services == total_services and active_alerts == 0 else 'warning',
                'uptime': self.get_system_uptime(),
                'active_services': active_services,
                'total_services': total_services,
                'active_alerts': active_alerts
            }
            
        except Exception as e:
            logger.error(f"獲取系統概覽失敗: {e}")
            return {
                'status': 'error',
                'uptime': '未知',
                'active_services': 0,
                'total_services': len(MONITORED_SERVICES),
                'active_alerts': 0
            }
    
    def get_system_uptime(self) -> str:
        """獲取系統運行時間"""
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            uptime_days = int(uptime_seconds // 86400)
            uptime_hours = int((uptime_seconds % 86400) // 3600)
            uptime_minutes = int((uptime_seconds % 3600) // 60)
            
            if uptime_days > 0:
                return f"{uptime_days}天 {uptime_hours}小時 {uptime_minutes}分鐘"
            elif uptime_hours > 0:
                return f"{uptime_hours}小時 {uptime_minutes}分鐘"
            else:
                return f"{uptime_minutes}分鐘"
                
        except Exception as e:
            logger.error(f"獲取系統運行時間失敗: {e}")
            return "未知"
    
    def get_services_status(self) -> List[Dict[str, Any]]:
        """獲取服務狀態"""
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            
            services = []
            for service_name, config in MONITORED_SERVICES.items():
                # 獲取最新狀態
                cursor.execute('''
                    SELECT status, response_time, details FROM service_status 
                    WHERE service_name = ? 
                    ORDER BY timestamp DESC LIMIT 1
                ''', (service_name,))
                
                result = cursor.fetchone()
                if result:
                    status, response_time, details = result
                    details_dict = json.loads(details) if details else {}
                else:
                    status = 'unknown'
                    response_time = None
                    details_dict = {}
                
                services.append({
                    'name': service_name,
                    'status': status,
                    'response_time': response_time,
                    'description': config['description'],
                    'port': config['port'],
                    'details': details_dict
                })
            
            conn.close()
            return services
            
        except Exception as e:
            logger.error(f"獲取服務狀態失敗: {e}")
            return []
    
    def get_system_resources(self) -> Dict[str, Any]:
        """獲取系統資源使用情況"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_percent': round(cpu_percent, 1),
                'memory_percent': round(memory.percent, 1),
                'memory_used_gb': round(memory.used / (1024**3), 2),
                'memory_total_gb': round(memory.total / (1024**3), 2),
                'disk_percent': round(disk.percent, 1),
                'disk_used_gb': round(disk.used / (1024**3), 2),
                'disk_total_gb': round(disk.total / (1024**3), 2)
            }
            
        except Exception as e:
            logger.error(f"獲取系統資源失敗: {e}")
            return {
                'cpu_percent': 0,
                'memory_percent': 0,
                'memory_used_gb': 0,
                'memory_total_gb': 0,
                'disk_percent': 0,
                'disk_used_gb': 0,
                'disk_total_gb': 0
            }
    
    def get_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """獲取告警列表"""
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, type, message, severity, resolved 
                FROM alerts 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            alerts = []
            for row in cursor.fetchall():
                timestamp, alert_type, message, severity, resolved = row
                alerts.append({
                    'timestamp': timestamp,
                    'type': alert_type,
                    'message': message,
                    'severity': severity,
                    'resolved': bool(resolved)
                })
            
            conn.close()
            return alerts
            
        except Exception as e:
            logger.error(f"獲取告警列表失敗: {e}")
            return []

# 初始化運營管理器
ops_manager = OperationsManager()

@app.route('/')
def index():
    """提供前台UI頁面"""
    return send_from_directory('frontend', 'index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({
        'service': 'operations_management_ui_backend',
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0'
    })

@app.route('/api/system/overview', methods=['GET'])
def get_system_overview():
    """獲取系統概覽API"""
    try:
        overview = ops_manager.get_system_overview()
        return jsonify(overview)
    except Exception as e:
        logger.error(f"系統概覽API錯誤: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/services/status', methods=['GET'])
def get_services_status():
    """獲取服務狀態API"""
    try:
        services = ops_manager.get_services_status()
        return jsonify({'services': services})
    except Exception as e:
        logger.error(f"服務狀態API錯誤: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/resources', methods=['GET'])
def get_system_resources():
    """獲取系統資源API"""
    try:
        resources = ops_manager.get_system_resources()
        return jsonify(resources)
    except Exception as e:
        logger.error(f"系統資源API錯誤: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """獲取告警列表API"""
    try:
        limit = request.args.get('limit', 10, type=int)
        alerts = ops_manager.get_alerts(limit)
        return jsonify({'alerts': alerts})
    except Exception as e:
        logger.error(f"告警列表API錯誤: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts/<int:alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    """解決告警API"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE alerts SET resolved = TRUE 
            WHERE id = ?
        ''', (alert_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': '告警已解決'})
    except Exception as e:
        logger.error(f"解決告警API錯誤: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("啟動運營管理中心後端服務...")
    app.run(host='0.0.0.0', port=5001, debug=False)

