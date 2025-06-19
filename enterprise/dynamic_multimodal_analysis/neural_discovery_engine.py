#!/usr/bin/env python3
"""
自進化 MCP 神經網路 - 神經發現引擎
Neural Discovery Engine for Self-Evolving MCP Neural Network

最小前置，最大自進化的核心實現
"""

import asyncio
import json
import time
import socket
import requests
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MCPNeuron:
    """MCP 神經元數據結構"""
    id: str
    host: str
    port: int
    capabilities: List[str]
    last_seen: datetime
    connection_strength: float = 0.5
    success_rate: float = 0.0
    response_time: float = 0.0
    is_active: bool = True

@dataclass
class NeuralConnection:
    """神經連接數據結構"""
    source_id: str
    target_id: str
    weight: float
    usage_count: int
    success_count: int
    last_used: datetime
    connection_type: str  # 'direct', 'relay', 'broadcast'

class NeuralDiscoveryEngine:
    """
    神經發現引擎
    
    核心功能：
    1. 自動發現網路中的 MCP 組件
    2. 評估組件能力和特性
    3. 建立和維護神經元註冊表
    4. 學習發現模式
    """
    
    def __init__(self, scan_range: Tuple[int, int] = (8090, 8099)):
        self.scan_range = scan_range
        self.discovered_neurons: Dict[str, MCPNeuron] = {}
        self.discovery_patterns: List[Dict] = []
        self.scan_interval = 30  # 秒
        self.is_running = False
        
        # 自進化參數
        self.learning_rate = 0.1
        self.discovery_success_threshold = 0.8
        self.neuron_timeout = 300  # 5分鐘無響應視為離線
        
    async def start_discovery(self):
        """啟動持續發現過程"""
        self.is_running = True
        logger.info("🧠 神經發現引擎啟動")
        
        while self.is_running:
            try:
                await self.discover_cycle()
                await asyncio.sleep(self.scan_interval)
            except Exception as e:
                logger.error(f"發現循環錯誤: {e}")
                await asyncio.sleep(5)
    
    async def discover_cycle(self):
        """單次發現循環"""
        logger.info("🔍 開始神經元發現循環")
        
        # 1. 掃描端口範圍
        new_neurons = await self.scan_port_range()
        
        # 2. 驗證已知神經元
        await self.verify_existing_neurons()
        
        # 3. 評估新發現的神經元
        for neuron in new_neurons:
            await self.evaluate_neuron(neuron)
        
        # 4. 學習發現模式
        self.learn_discovery_patterns()
        
        # 5. 優化掃描策略
        self.optimize_scan_strategy()
        
        logger.info(f"🧠 發現循環完成，當前神經元數量: {len(self.discovered_neurons)}")
    
    async def scan_port_range(self) -> List[MCPNeuron]:
        """掃描端口範圍發現新的 MCP 組件"""
        new_neurons = []
        
        for port in range(self.scan_range[0], self.scan_range[1] + 1):
            try:
                # 檢查端口是否開放
                if await self.is_port_open('localhost', port):
                    # 嘗試獲取 MCP 信息
                    neuron_info = await self.probe_mcp_service(port)
                    if neuron_info:
                        neuron_id = f"mcp_{port}"
                        
                        # 如果是新神經元
                        if neuron_id not in self.discovered_neurons:
                            neuron = MCPNeuron(
                                id=neuron_id,
                                host='localhost',
                                port=port,
                                capabilities=neuron_info.get('capabilities', []),
                                last_seen=datetime.now()
                            )
                            new_neurons.append(neuron)
                            logger.info(f"🆕 發現新神經元: {neuron_id} (端口 {port})")
                        else:
                            # 更新已知神經元的最後見到時間
                            self.discovered_neurons[neuron_id].last_seen = datetime.now()
                            
            except Exception as e:
                logger.debug(f"掃描端口 {port} 時出錯: {e}")
        
        return new_neurons
    
    async def is_port_open(self, host: str, port: int, timeout: float = 1.0) -> bool:
        """檢查端口是否開放"""
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=timeout
            )
            writer.close()
            await writer.wait_closed()
            return True
        except:
            return False
    
    async def probe_mcp_service(self, port: int) -> Optional[Dict]:
        """探測 MCP 服務信息"""
        try:
            # 嘗試常見的健康檢查端點
            health_endpoints = ['/api/health', '/health', '/status', '/']
            
            for endpoint in health_endpoints:
                try:
                    response = requests.get(
                        f"http://localhost:{port}{endpoint}",
                        timeout=2
                    )
                    if response.status_code == 200:
                        data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                        
                        # 提取 MCP 能力信息
                        capabilities = []
                        if 'capabilities' in data:
                            capabilities = data['capabilities']
                        elif 'service' in data:
                            capabilities = [data['service']]
                        
                        return {
                            'capabilities': capabilities,
                            'service_info': data,
                            'endpoint': endpoint
                        }
                except:
                    continue
                    
        except Exception as e:
            logger.debug(f"探測端口 {port} 服務時出錯: {e}")
        
        return None
    
    async def verify_existing_neurons(self):
        """驗證已知神經元的狀態"""
        current_time = datetime.now()
        inactive_neurons = []
        
        for neuron_id, neuron in self.discovered_neurons.items():
            try:
                # 檢查神經元是否仍然活躍
                if await self.is_port_open(neuron.host, neuron.port, timeout=0.5):
                    neuron.last_seen = current_time
                    neuron.is_active = True
                else:
                    # 檢查是否超時
                    if (current_time - neuron.last_seen).seconds > self.neuron_timeout:
                        neuron.is_active = False
                        inactive_neurons.append(neuron_id)
                        
            except Exception as e:
                logger.debug(f"驗證神經元 {neuron_id} 時出錯: {e}")
        
        # 移除不活躍的神經元
        for neuron_id in inactive_neurons:
            logger.info(f"🔴 神經元離線: {neuron_id}")
            del self.discovered_neurons[neuron_id]
    
    async def evaluate_neuron(self, neuron: MCPNeuron):
        """評估新神經元的能力和特性"""
        try:
            # 測試響應時間
            start_time = time.time()
            response = requests.get(f"http://{neuron.host}:{neuron.port}/api/health", timeout=5)
            neuron.response_time = time.time() - start_time
            
            if response.status_code == 200:
                neuron.success_rate = 1.0
                
                # 嘗試獲取更詳細的能力信息
                try:
                    data = response.json()
                    if 'capabilities' in data:
                        neuron.capabilities.extend(data['capabilities'])
                    neuron.capabilities = list(set(neuron.capabilities))  # 去重
                except:
                    pass
                
                # 註冊新神經元
                self.discovered_neurons[neuron.id] = neuron
                logger.info(f"✅ 神經元註冊成功: {neuron.id}")
                
            else:
                logger.warning(f"⚠️ 神經元響應異常: {neuron.id} (狀態碼: {response.status_code})")
                
        except Exception as e:
            logger.error(f"❌ 評估神經元 {neuron.id} 失敗: {e}")
    
    def learn_discovery_patterns(self):
        """學習發現模式，優化未來的發現策略"""
        # 分析成功的發現模式
        successful_ports = [neuron.port for neuron in self.discovered_neurons.values() if neuron.is_active]
        
        if len(successful_ports) > 0:
            # 學習端口分佈模式
            port_pattern = {
                'common_ports': successful_ports,
                'port_range': (min(successful_ports), max(successful_ports)),
                'discovery_time': datetime.now(),
                'success_rate': len(successful_ports) / (self.scan_range[1] - self.scan_range[0] + 1)
            }
            
            self.discovery_patterns.append(port_pattern)
            
            # 保持最近的模式記錄
            if len(self.discovery_patterns) > 10:
                self.discovery_patterns = self.discovery_patterns[-10:]
    
    def optimize_scan_strategy(self):
        """基於學習到的模式優化掃描策略"""
        if len(self.discovery_patterns) >= 3:
            # 分析最近的模式
            recent_patterns = self.discovery_patterns[-3:]
            
            # 計算平均成功率
            avg_success_rate = sum(p['success_rate'] for p in recent_patterns) / len(recent_patterns)
            
            # 調整掃描間隔
            if avg_success_rate > self.discovery_success_threshold:
                # 成功率高，可以降低掃描頻率
                self.scan_interval = min(self.scan_interval * 1.2, 60)
            else:
                # 成功率低，增加掃描頻率
                self.scan_interval = max(self.scan_interval * 0.8, 10)
            
            logger.info(f"🎯 優化掃描策略: 間隔={self.scan_interval}秒, 成功率={avg_success_rate:.2f}")
    
    def get_active_neurons(self) -> Dict[str, MCPNeuron]:
        """獲取所有活躍的神經元"""
        return {nid: neuron for nid, neuron in self.discovered_neurons.items() if neuron.is_active}
    
    def get_neurons_by_capability(self, capability: str) -> List[MCPNeuron]:
        """根據能力獲取神經元"""
        return [neuron for neuron in self.discovered_neurons.values() 
                if neuron.is_active and capability in neuron.capabilities]
    
    def stop_discovery(self):
        """停止發現過程"""
        self.is_running = False
        logger.info("🛑 神經發現引擎停止")
    
    def get_discovery_stats(self) -> Dict:
        """獲取發現統計信息"""
        active_neurons = self.get_active_neurons()
        
        return {
            'total_neurons': len(self.discovered_neurons),
            'active_neurons': len(active_neurons),
            'discovery_patterns': len(self.discovery_patterns),
            'scan_interval': self.scan_interval,
            'capabilities': list(set(cap for neuron in active_neurons.values() for cap in neuron.capabilities)),
            'last_discovery': max([neuron.last_seen for neuron in active_neurons.values()]) if active_neurons else None
        }

# 測試和演示代碼
async def main():
    """測試神經發現引擎"""
    engine = NeuralDiscoveryEngine()
    
    # 啟動發現引擎
    discovery_task = asyncio.create_task(engine.start_discovery())
    
    try:
        # 運行一段時間進行測試
        await asyncio.sleep(60)  # 運行1分鐘
        
        # 顯示發現結果
        stats = engine.get_discovery_stats()
        print("\n🧠 神經發現引擎統計:")
        print(json.dumps(stats, indent=2, default=str))
        
        # 顯示發現的神經元
        active_neurons = engine.get_active_neurons()
        print(f"\n🔗 發現的活躍神經元 ({len(active_neurons)}):")
        for neuron_id, neuron in active_neurons.items():
            print(f"  {neuron_id}: {neuron.host}:{neuron.port} - {neuron.capabilities}")
        
    finally:
        engine.stop_discovery()
        discovery_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())

