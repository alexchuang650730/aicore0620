"""
Advanced SmartUI - 整合版智慧感知 UI MCP 適配器

整合了 React SmartUI 前端和 Enhanced SmartUI 後端的完整解決方案
"""

import asyncio
import json
import logging
import subprocess
import threading
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import websocket
import requests

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SmartUIRequest:
    """SmartUI 請求數據結構"""
    request_id: str
    request_type: str  # "ui_generation", "voice_command", "layout_optimization"
    user_input: Dict[str, Any]
    context: Dict[str, Any]
    target_components: List[str]

@dataclass
class SmartUIResponse:
    """SmartUI 回應數據結構"""
    request_id: str
    status: str  # "success", "error", "processing"
    result: Dict[str, Any]
    ui_updates: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class AdvancedSmartUIAdapter:
    """Advanced SmartUI MCP 適配器"""
    
    def __init__(self, backend_port: int = 8097, frontend_port: int = 3002):
        self.backend_port = backend_port
        self.frontend_port = frontend_port
        self.app = Flask(__name__)
        CORS(self.app)
        
        # 組件路徑
        self.base_path = Path(__file__).parent
        self.backend_path = self.base_path
        self.frontend_path = self.base_path / "frontend"
        
        # 狀態管理
        self.active_sessions = {}
        self.ui_state = {}
        
        # 初始化路由
        self._setup_routes()
        
        # 後端和前端進程
        self.backend_process = None
        self.frontend_process = None
        
    def _setup_routes(self):
        """設置 API 路由"""
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """健康檢查"""
            return jsonify({
                "status": "healthy",
                "adapter": "advanced_smartui",
                "backend_port": self.backend_port,
                "frontend_port": self.frontend_port,
                "capabilities": [
                    "ui_generation",
                    "voice_control", 
                    "layout_optimization",
                    "real_time_updates",
                    "mcp_integration"
                ]
            })
        
        @self.app.route('/api/execute', methods=['POST'])
        def execute_smartui_request():
            """執行 SmartUI 請求"""
            try:
                request_data = request.get_json()
                smartui_request = SmartUIRequest(**request_data)
                
                # 處理請求
                response = self._process_smartui_request(smartui_request)
                
                return jsonify(response.__dict__)
                
            except Exception as e:
                logger.error(f"執行 SmartUI 請求失敗: {e}")
                return jsonify({
                    "status": "error",
                    "error_message": str(e)
                }), 500
        
        @self.app.route('/api/ui/command', methods=['POST'])
        def handle_ui_command():
            """處理 UI 指令"""
            try:
                command_data = request.get_json()
                result = self._handle_ui_command(command_data)
                return jsonify(result)
            except Exception as e:
                logger.error(f"處理 UI 指令失敗: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/ui/state', methods=['GET', 'POST'])
        def manage_ui_state():
            """管理 UI 狀態"""
            if request.method == 'GET':
                return jsonify(self.ui_state)
            else:
                try:
                    new_state = request.get_json()
                    self.ui_state.update(new_state)
                    return jsonify({"status": "updated"})
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
        
        @self.app.route('/frontend/<path:filename>')
        def serve_frontend(filename):
            """提供前端靜態文件"""
            return send_from_directory(self.frontend_path / "dist", filename)
    
    def _process_smartui_request(self, smartui_request: SmartUIRequest) -> SmartUIResponse:
        """處理 SmartUI 請求"""
        try:
            if smartui_request.request_type == "ui_generation":
                return self._handle_ui_generation(smartui_request)
            elif smartui_request.request_type == "voice_command":
                return self._handle_voice_command(smartui_request)
            elif smartui_request.request_type == "layout_optimization":
                return self._handle_layout_optimization(smartui_request)
            else:
                return SmartUIResponse(
                    request_id=smartui_request.request_id,
                    status="error",
                    result={},
                    error_message=f"不支援的請求類型: {smartui_request.request_type}"
                )
        except Exception as e:
            logger.error(f"處理 SmartUI 請求失敗: {e}")
            return SmartUIResponse(
                request_id=smartui_request.request_id,
                status="error",
                result={},
                error_message=str(e)
            )
    
    def _handle_ui_generation(self, request: SmartUIRequest) -> SmartUIResponse:
        """處理 UI 生成請求"""
        # 調用後端 Enhanced SmartUI 的 UI 生成功能
        try:
            backend_response = requests.post(
                f"http://localhost:{self.backend_port}/api/generate_ui",
                json=request.user_input,
                timeout=30
            )
            
            if backend_response.status_code == 200:
                ui_config = backend_response.json()
                
                # 更新前端狀態
                self._update_frontend_ui(ui_config)
                
                return SmartUIResponse(
                    request_id=request.request_id,
                    status="success",
                    result=ui_config,
                    ui_updates=ui_config
                )
            else:
                raise Exception(f"後端 UI 生成失敗: {backend_response.status_code}")
                
        except Exception as e:
            logger.error(f"UI 生成失敗: {e}")
            return SmartUIResponse(
                request_id=request.request_id,
                status="error",
                result={},
                error_message=str(e)
            )
    
    def _handle_voice_command(self, request: SmartUIRequest) -> SmartUIResponse:
        """處理語音指令"""
        voice_command = request.user_input.get("command", "")
        
        # 解析語音指令
        parsed_command = self._parse_voice_command(voice_command)
        
        # 執行指令
        result = self._execute_command(parsed_command)
        
        return SmartUIResponse(
            request_id=request.request_id,
            status="success",
            result=result
        )
    
    def _handle_layout_optimization(self, request: SmartUIRequest) -> SmartUIResponse:
        """處理佈局優化"""
        layout_config = request.user_input.get("layout_config", {})
        
        # 調用佈局優化算法
        optimized_layout = self._optimize_layout(layout_config)
        
        # 更新前端佈局
        self._update_frontend_layout(optimized_layout)
        
        return SmartUIResponse(
            request_id=request.request_id,
            status="success",
            result=optimized_layout,
            ui_updates={"layout": optimized_layout}
        )
    
    def _handle_ui_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """處理 UI 指令"""
        command_type = command_data.get("type")
        
        if command_type == "node_click":
            node_type = command_data.get("node_type")
            return self._handle_node_click(node_type)
        elif command_type == "voice_control":
            return self._handle_voice_control_toggle()
        elif command_type == "layout_change":
            layout_type = command_data.get("layout_type")
            return self._handle_layout_change(layout_type)
        else:
            return {"error": f"未知的指令類型: {command_type}"}
    
    def _handle_node_click(self, node_type: str) -> Dict[str, Any]:
        """處理節點點擊"""
        # 更新節點狀態
        if node_type not in self.ui_state:
            self.ui_state[node_type] = {}
        
        self.ui_state[node_type]["last_clicked"] = time.time()
        self.ui_state[node_type]["status"] = "active"
        
        return {
            "status": "success",
            "node_type": node_type,
            "updated_state": self.ui_state[node_type]
        }
    
    def _parse_voice_command(self, command: str) -> Dict[str, Any]:
        """解析語音指令"""
        # 簡單的指令解析邏輯
        command_lower = command.lower()
        
        if "編碼" in command_lower or "coding" in command_lower:
            return {"action": "activate_node", "target": "coding"}
        elif "測試" in command_lower or "testing" in command_lower:
            return {"action": "activate_node", "target": "testing"}
        elif "部署" in command_lower or "deployment" in command_lower:
            return {"action": "activate_node", "target": "deployment"}
        elif "狀態" in command_lower or "status" in command_lower:
            return {"action": "show_status"}
        else:
            return {"action": "unknown", "original_command": command}
    
    def _execute_command(self, parsed_command: Dict[str, Any]) -> Dict[str, Any]:
        """執行解析後的指令"""
        action = parsed_command.get("action")
        
        if action == "activate_node":
            target = parsed_command.get("target")
            return self._handle_node_click(target)
        elif action == "show_status":
            return {"status": "success", "ui_state": self.ui_state}
        else:
            return {"status": "error", "message": "無法執行指令"}
    
    def _optimize_layout(self, layout_config: Dict[str, Any]) -> Dict[str, Any]:
        """優化佈局"""
        # 佈局優化邏輯
        optimized = layout_config.copy()
        optimized["optimized"] = True
        optimized["optimization_timestamp"] = time.time()
        
        return optimized
    
    def _update_frontend_ui(self, ui_config: Dict[str, Any]):
        """更新前端 UI"""
        # 通過 WebSocket 或 API 更新前端
        try:
            requests.post(
                f"http://localhost:{self.frontend_port}/api/update_ui",
                json=ui_config,
                timeout=5
            )
        except Exception as e:
            logger.warning(f"更新前端 UI 失敗: {e}")
    
    def _update_frontend_layout(self, layout_config: Dict[str, Any]):
        """更新前端佈局"""
        try:
            requests.post(
                f"http://localhost:{self.frontend_port}/api/update_layout",
                json=layout_config,
                timeout=5
            )
        except Exception as e:
            logger.warning(f"更新前端佈局失敗: {e}")
    
    def start_backend(self):
        """啟動後端服務"""
        try:
            backend_script = self.backend_path / "main_server.py"
            self.backend_process = subprocess.Popen([
                "python", str(backend_script)
            ], cwd=str(self.backend_path))
            logger.info(f"後端服務已啟動，PID: {self.backend_process.pid}")
        except Exception as e:
            logger.error(f"啟動後端服務失敗: {e}")
    
    def start_frontend(self):
        """啟動前端服務"""
        try:
            self.frontend_process = subprocess.Popen([
                "npm", "run", "dev"
            ], cwd=str(self.frontend_path))
            logger.info(f"前端服務已啟動，PID: {self.frontend_process.pid}")
        except Exception as e:
            logger.error(f"啟動前端服務失敗: {e}")
    
    def start(self):
        """啟動 Advanced SmartUI 適配器"""
        logger.info("啟動 Advanced SmartUI 適配器...")
        
        # 啟動後端和前端服務
        self.start_backend()
        time.sleep(2)  # 等待後端啟動
        self.start_frontend()
        
        # 啟動適配器 API 服務
        self.app.run(host='0.0.0.0', port=8098, debug=False)
    
    def stop(self):
        """停止適配器"""
        logger.info("停止 Advanced SmartUI 適配器...")
        
        if self.backend_process:
            self.backend_process.terminate()
        if self.frontend_process:
            self.frontend_process.terminate()

if __name__ == "__main__":
    adapter = AdvancedSmartUIAdapter()
    try:
        adapter.start()
    except KeyboardInterrupt:
        adapter.stop()

