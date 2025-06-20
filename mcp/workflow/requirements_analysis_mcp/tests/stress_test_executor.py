#!/usr/bin/env python3
"""
AI需求分析系統壓力測試執行器
基於PowerAutomation MCP測試框架的標準測試用例

測試用例ID: TC001-TC007
測試目標: 診斷系統錯誤、端口問題和僵屍進程問題
"""

import asyncio
import aiohttp
import json
import time
import psutil
import subprocess
import threading
import sys
import os
from datetime import datetime
from pathlib import Path
import logging

# 添加MCP路徑
sys.path.append('/home/ubuntu/aicore0620/mcp/workflow/requirements_analysis_mcp')

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/aicore0620/mcp/workflow/requirements_analysis_mcp/testcases/stress_test_execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('StressTestCase')

class PowerAutomationStressTestCase:
    """
    PowerAutomation MCP框架標準壓力測試用例
    符合requirements_analysis_mcp測試規範
    """
    
    def __init__(self):
        self.test_case_id = "STRESS_TEST_SUITE"
        self.test_version = "1.0.0"
        self.test_framework = "PowerAutomation MCP"
        
        # 測試目標服務
        self.test_servers = [
            {"name": "本地UI服務", "url": "http://localhost:5001", "type": "ui"},
            {"name": "EC2 UI服務", "url": "http://18.212.97.173:5001", "type": "ui"}
        ]
        
        self.ai_engines = [
            {"name": "本地AI引擎", "url": "http://localhost:8888", "type": "ai_engine"},
            {"name": "EC2 AI引擎", "url": "http://18.212.97.173:8888", "type": "ai_engine"}
        ]
        
        # 測試數據
        self.test_document = "這個核保的整份文件的sop 大概大概要花多少人處理表單,自動化比率在業界有多高,表單ocr 用人來審核在整個sop流程所佔的人月大概是多少"
        
        # 測試結果收集
        self.test_results = {
            "test_suite": self.test_case_id,
            "test_version": self.test_version,
            "start_time": None,
            "end_time": None,
            "test_cases": {},
            "summary": {}
        }
    
    async def tc001_service_health_check(self):
        """TC001: 服務健康狀態檢查"""
        logger.info("執行 TC001: 服務健康狀態檢查")
        
        test_result = {
            "test_case_id": "TC001",
            "test_name": "服務健康狀態檢查",
            "status": "RUNNING",
            "start_time": datetime.now().isoformat(),
            "checks": []
        }
        
        try:
            # 檢查所有服務
            all_services = self.test_servers + self.ai_engines
            
            for service in all_services:
                check_start = time.time()
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"{service['url']}/health", timeout=5) as response:
                            check_time = time.time() - check_start
                            
                            if response.status == 200:
                                data = await response.json()
                                test_result["checks"].append({
                                    "service": service["name"],
                                    "url": service["url"],
                                    "status": "PASS",
                                    "response_time": check_time,
                                    "data": data
                                })
                            else:
                                test_result["checks"].append({
                                    "service": service["name"],
                                    "url": service["url"],
                                    "status": "FAIL",
                                    "error": f"HTTP {response.status}",
                                    "response_time": check_time
                                })
                except Exception as e:
                    check_time = time.time() - check_start
                    test_result["checks"].append({
                        "service": service["name"],
                        "url": service["url"],
                        "status": "ERROR",
                        "error": str(e),
                        "response_time": check_time
                    })
            
            # 評估測試結果
            passed_checks = len([c for c in test_result["checks"] if c["status"] == "PASS"])
            total_checks = len(test_result["checks"])
            
            if passed_checks == total_checks:
                test_result["status"] = "PASS"
                test_result["result"] = "所有服務健康狀態正常"
            else:
                test_result["status"] = "FAIL"
                test_result["result"] = f"健康檢查失敗: {passed_checks}/{total_checks} 服務正常"
            
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["error"] = str(e)
        
        test_result["end_time"] = datetime.now().isoformat()
        return test_result
    
    async def tc002_light_stress_test(self):
        """TC002: 輕量壓力測試"""
        logger.info("執行 TC002: 輕量壓力測試")
        
        return await self._execute_stress_test(
            test_case_id="TC002",
            test_name="輕量壓力測試",
            num_requests=5,
            concurrency=2,
            expected_success_rate=90
        )
    
    async def tc003_medium_stress_test(self):
        """TC003: 中等負載壓力測試"""
        logger.info("執行 TC003: 中等負載壓力測試")
        
        return await self._execute_stress_test(
            test_case_id="TC003",
            test_name="中等負載壓力測試",
            num_requests=10,
            concurrency=5,
            expected_success_rate=85
        )
    
    async def tc004_heavy_stress_test(self):
        """TC004: 高負載壓力測試"""
        logger.info("執行 TC004: 高負載壓力測試")
        
        return await self._execute_stress_test(
            test_case_id="TC004",
            test_name="高負載壓力測試",
            num_requests=20,
            concurrency=10,
            expected_success_rate=80
        )
    
    async def _execute_stress_test(self, test_case_id, test_name, num_requests, concurrency, expected_success_rate):
        """執行壓力測試的通用方法"""
        test_result = {
            "test_case_id": test_case_id,
            "test_name": test_name,
            "status": "RUNNING",
            "start_time": datetime.now().isoformat(),
            "parameters": {
                "num_requests": num_requests,
                "concurrency": concurrency,
                "expected_success_rate": expected_success_rate
            }
        }
        
        try:
            # 記錄測試前狀態
            initial_processes = self._monitor_processes()
            initial_ports = self._monitor_ports()
            initial_zombies = self._check_zombie_processes()
            
            # 創建並發任務
            tasks = []
            semaphore = asyncio.Semaphore(concurrency)
            
            async def limited_request(server_url, request_id):
                async with semaphore:
                    return await self._send_analysis_request(server_url, request_id)
            
            # 為每個服務器創建請求任務
            request_id = 0
            for server in self.test_servers:
                for i in range(num_requests):
                    task = limited_request(server["url"], request_id)
                    tasks.append(task)
                    request_id += 1
            
            # 執行並發測試
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            end_time = time.time()
            
            # 記錄測試後狀態
            final_processes = self._monitor_processes()
            final_ports = self._monitor_ports()
            final_zombies = self._check_zombie_processes()
            
            # 分析結果
            successful_requests = [r for r in results if isinstance(r, dict) and r.get('status') == 'success']
            failed_requests = [r for r in results if isinstance(r, dict) and r.get('status') != 'success']
            exceptions = [r for r in results if isinstance(r, Exception)]
            
            success_rate = len(successful_requests) / len(tasks) * 100
            avg_response_time = sum(r.get('response_time', 0) for r in successful_requests) / max(len(successful_requests), 1)
            
            test_result.update({
                "metrics": {
                    "test_duration": end_time - start_time,
                    "total_requests": len(tasks),
                    "successful_requests": len(successful_requests),
                    "failed_requests": len(failed_requests),
                    "exceptions": len(exceptions),
                    "success_rate": success_rate,
                    "average_response_time": avg_response_time
                },
                "system_state": {
                    "initial": {
                        "processes": len(initial_processes),
                        "ports": initial_ports,
                        "zombies": len(initial_zombies)
                    },
                    "final": {
                        "processes": len(final_processes),
                        "ports": final_ports,
                        "zombies": len(final_zombies)
                    },
                    "changes": {
                        "process_changes": len(final_processes) - len(initial_processes),
                        "new_zombies": len(final_zombies) - len(initial_zombies)
                    }
                }
            })
            
            # 評估測試結果
            if success_rate >= expected_success_rate and test_result["system_state"]["changes"]["new_zombies"] == 0:
                test_result["status"] = "PASS"
                test_result["result"] = f"壓力測試通過: 成功率{success_rate:.1f}%, 響應時間{avg_response_time:.2f}秒"
            else:
                test_result["status"] = "FAIL"
                test_result["result"] = f"壓力測試失敗: 成功率{success_rate:.1f}% (期望≥{expected_success_rate}%)"
            
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["error"] = str(e)
        
        test_result["end_time"] = datetime.now().isoformat()
        return test_result
    
    async def tc005_zombie_process_monitoring(self):
        """TC005: 僵屍進程監控測試"""
        logger.info("執行 TC005: 僵屍進程監控測試")
        
        test_result = {
            "test_case_id": "TC005",
            "test_name": "僵屍進程監控測試",
            "status": "RUNNING",
            "start_time": datetime.now().isoformat()
        }
        
        try:
            # 檢查僵屍進程
            zombie_processes = self._check_zombie_processes()
            
            test_result.update({
                "zombie_processes": zombie_processes,
                "zombie_count": len(zombie_processes),
                "monitoring_result": "僵屍進程監控完成"
            })
            
            # 評估結果 - 允許存在系統級僵屍進程
            if len(zombie_processes) <= 1:  # 允許1個系統級僵屍進程
                test_result["status"] = "PASS"
                test_result["result"] = f"僵屍進程數量正常: {len(zombie_processes)}個"
            else:
                test_result["status"] = "FAIL"
                test_result["result"] = f"僵屍進程數量異常: {len(zombie_processes)}個"
            
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["error"] = str(e)
        
        test_result["end_time"] = datetime.now().isoformat()
        return test_result
    
    async def tc006_port_monitoring(self):
        """TC006: 端口狀態監控測試"""
        logger.info("執行 TC006: 端口狀態監控測試")
        
        test_result = {
            "test_case_id": "TC006",
            "test_name": "端口狀態監控測試",
            "status": "RUNNING",
            "start_time": datetime.now().isoformat()
        }
        
        try:
            # 監控關鍵端口
            port_status = self._monitor_ports()
            
            test_result.update({
                "port_status": port_status,
                "monitoring_result": "端口狀態監控完成"
            })
            
            # 評估結果
            required_ports = [5001, 8888]
            all_ports_ok = all(port_status.get(port, {}).get('listening', False) for port in required_ports)
            
            if all_ports_ok:
                test_result["status"] = "PASS"
                test_result["result"] = "所有關鍵端口狀態正常"
            else:
                test_result["status"] = "FAIL"
                test_result["result"] = "部分關鍵端口狀態異常"
            
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["error"] = str(e)
        
        test_result["end_time"] = datetime.now().isoformat()
        return test_result
    
    async def tc007_api_functionality_test(self):
        """TC007: API功能驗證測試"""
        logger.info("執行 TC007: API功能驗證測試")
        
        test_result = {
            "test_case_id": "TC007",
            "test_name": "API功能驗證測試",
            "status": "RUNNING",
            "start_time": datetime.now().isoformat(),
            "api_tests": []
        }
        
        try:
            # 測試每個API端點
            for server in self.test_servers:
                api_test = await self._test_api_functionality(server["url"], server["name"])
                test_result["api_tests"].append(api_test)
            
            # 評估結果
            passed_tests = len([t for t in test_result["api_tests"] if t["status"] == "PASS"])
            total_tests = len(test_result["api_tests"])
            
            if passed_tests == total_tests:
                test_result["status"] = "PASS"
                test_result["result"] = "所有API功能正常"
            else:
                test_result["status"] = "FAIL"
                test_result["result"] = f"API功能測試失敗: {passed_tests}/{total_tests} 通過"
            
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["error"] = str(e)
        
        test_result["end_time"] = datetime.now().isoformat()
        return test_result
    
    async def _send_analysis_request(self, server_url: str, request_id: int) -> dict:
        """發送分析請求"""
        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "requirement": self.test_document,
                    "test_id": request_id
                }
                
                async with session.post(
                    f"{server_url}/api/analyze",
                    json=payload,
                    timeout=30
                ) as response:
                    end_time = time.time()
                    response_time = end_time - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "request_id": request_id,
                            "server": server_url,
                            "status": "success",
                            "response_time": response_time,
                            "data": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "request_id": request_id,
                            "server": server_url,
                            "status": "error",
                            "response_time": response_time,
                            "error": f"HTTP {response.status}: {error_text}",
                            "timestamp": datetime.now().isoformat()
                        }
                        
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            return {
                "request_id": request_id,
                "server": server_url,
                "status": "exception",
                "response_time": response_time,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _test_api_functionality(self, server_url: str, server_name: str) -> dict:
        """測試API功能"""
        try:
            result = await self._send_analysis_request(server_url, 999)
            
            if result["status"] == "success":
                # 檢查返回數據的完整性
                data = result.get("data", {})
                has_analysis = "analysis" in data
                has_confidence = "confidence_score" in data
                
                if has_analysis and has_confidence:
                    return {
                        "server": server_name,
                        "url": server_url,
                        "status": "PASS",
                        "response_time": result["response_time"],
                        "result": "API功能正常"
                    }
                else:
                    return {
                        "server": server_name,
                        "url": server_url,
                        "status": "FAIL",
                        "response_time": result["response_time"],
                        "result": "API返回數據不完整"
                    }
            else:
                return {
                    "server": server_name,
                    "url": server_url,
                    "status": "FAIL",
                    "error": result.get("error", "未知錯誤"),
                    "result": "API調用失敗"
                }
                
        except Exception as e:
            return {
                "server": server_name,
                "url": server_url,
                "status": "ERROR",
                "error": str(e),
                "result": "API測試異常"
            }
    
    def _monitor_processes(self):
        """監控系統進程"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if any(keyword in cmdline.lower() for keyword in ['sandbox_server', 'flask', 'python3']):
                        if any(port in cmdline for port in ['5001', '8888']):
                            processes.append({
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'cmdline': cmdline,
                                'status': proc.info['status'],
                                'cpu_percent': proc.info['cpu_percent'],
                                'memory_percent': proc.info['memory_percent'],
                                'timestamp': datetime.now().isoformat()
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return processes
        except Exception as e:
            logger.error(f"進程監控錯誤: {e}")
            return []
    
    def _monitor_ports(self):
        """監控端口狀態"""
        try:
            port_status = {}
            target_ports = [5001, 8888]
            
            for port in target_ports:
                result = subprocess.run(
                    ['netstat', '-tlnp'], 
                    capture_output=True, 
                    text=True
                )
                
                port_listening = f":{port} " in result.stdout
                port_status[port] = {
                    'listening': port_listening,
                    'timestamp': datetime.now().isoformat()
                }
                
                if port_listening:
                    for line in result.stdout.split('\n'):
                        if f":{port} " in line:
                            parts = line.split()
                            if len(parts) >= 7:
                                port_status[port]['process_info'] = parts[6]
                            break
            
            return port_status
        except Exception as e:
            logger.error(f"端口監控錯誤: {e}")
            return {}
    
    def _check_zombie_processes(self):
        """檢查僵屍進程"""
        try:
            zombie_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'status', 'cmdline']):
                try:
                    if proc.info['status'] == psutil.STATUS_ZOMBIE:
                        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                        zombie_processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cmdline': cmdline,
                            'timestamp': datetime.now().isoformat()
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return zombie_processes
        except Exception as e:
            logger.error(f"僵屍進程檢查錯誤: {e}")
            return []
    
    async def run_test_suite(self):
        """執行完整的測試套件"""
        logger.info("=== PowerAutomation MCP 壓力測試套件開始 ===")
        
        self.test_results["start_time"] = datetime.now().isoformat()
        
        # 定義測試用例
        test_cases = [
            ("TC001", self.tc001_service_health_check),
            ("TC002", self.tc002_light_stress_test),
            ("TC003", self.tc003_medium_stress_test),
            ("TC004", self.tc004_heavy_stress_test),
            ("TC005", self.tc005_zombie_process_monitoring),
            ("TC006", self.tc006_port_monitoring),
            ("TC007", self.tc007_api_functionality_test)
        ]
        
        # 執行測試用例
        for test_id, test_func in test_cases:
            try:
                result = await test_func()
                self.test_results["test_cases"][test_id] = result
                
                status_symbol = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
                logger.info(f"{status_symbol} {test_id}: {result['test_name']} - {result['status']}")
                
                # 等待系統穩定
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"測試用例 {test_id} 執行失敗: {e}")
                self.test_results["test_cases"][test_id] = {
                    "test_case_id": test_id,
                    "status": "ERROR",
                    "error": str(e)
                }
        
        self.test_results["end_time"] = datetime.now().isoformat()
        
        # 生成測試摘要
        self._generate_test_summary()
        
        return self.test_results
    
    def _generate_test_summary(self):
        """生成測試摘要"""
        total_tests = len(self.test_results["test_cases"])
        passed_tests = len([t for t in self.test_results["test_cases"].values() if t["status"] == "PASS"])
        failed_tests = len([t for t in self.test_results["test_cases"].values() if t["status"] == "FAIL"])
        error_tests = len([t for t in self.test_results["test_cases"].values() if t["status"] == "ERROR"])
        
        self.test_results["summary"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "error_tests": error_tests,
            "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "overall_status": "PASS" if failed_tests == 0 and error_tests == 0 else "FAIL"
        }

def main():
    """主函數"""
    test_case = PowerAutomationStressTestCase()
    
    # 執行測試套件
    results = asyncio.run(test_case.run_test_suite())
    
    # 保存結果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = f"/home/ubuntu/aicore0620/mcp/workflow/requirements_analysis_mcp/testcases/stress_test_results_{timestamp}.json"
    
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    logger.info(f"測試結果已保存到: {result_file}")
    
    # 打印測試摘要
    summary = results["summary"]
    print(f"\n=== PowerAutomation MCP 測試套件結果 ===")
    print(f"測試框架: {test_case.test_framework}")
    print(f"測試版本: {test_case.test_version}")
    print(f"總測試數: {summary['total_tests']}")
    print(f"通過測試: {summary['passed_tests']}")
    print(f"失敗測試: {summary['failed_tests']}")
    print(f"錯誤測試: {summary['error_tests']}")
    print(f"通過率: {summary['pass_rate']:.1f}%")
    print(f"整體狀態: {'✅ PASS' if summary['overall_status'] == 'PASS' else '❌ FAIL'}")

if __name__ == "__main__":
    main()

