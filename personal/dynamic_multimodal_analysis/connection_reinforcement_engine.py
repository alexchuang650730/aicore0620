#!/usr/bin/env python3
"""
自進化 MCP 神經網路 - 連接強化機制
Connection Reinforcement Mechanism for Self-Evolving MCP Neural Network

基於使用模式和成功率動態調整神經元連接強度
"""

import asyncio
import json
import time
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class ConnectionMetrics:
    """連接指標數據結構"""
    total_attempts: int = 0
    successful_attempts: int = 0
    failed_attempts: int = 0
    total_response_time: float = 0.0
    last_success_time: Optional[datetime] = None
    last_failure_time: Optional[datetime] = None
    consecutive_failures: int = 0
    consecutive_successes: int = 0

@dataclass
class NeuralConnection:
    """神經連接數據結構"""
    source_id: str
    target_id: str
    weight: float
    connection_type: str
    created_time: datetime
    last_used: datetime
    metrics: ConnectionMetrics
    is_active: bool = True

class ConnectionReinforcementEngine:
    """
    連接強化引擎
    
    核心功能：
    1. 根據使用模式強化有效連接
    2. 弱化或移除低效連接
    3. 動態調整連接權重
    4. 學習最佳連接模式
    """
    
    def __init__(self):
        self.connections: Dict[str, NeuralConnection] = {}
        self.reinforcement_history: List[Dict] = []
        
        # 強化學習參數
        self.learning_rate = 0.1
        self.reinforcement_threshold = 0.8
        self.pruning_threshold = 0.2
        self.decay_rate = 0.01  # 權重衰減率
        self.max_weight = 1.0
        self.min_weight = 0.1
        
        # 連接評估參數
        self.success_rate_weight = 0.4
        self.response_time_weight = 0.3
        self.usage_frequency_weight = 0.3
        
        # 自適應參數
        self.adaptation_cycle = 3600  # 1小時
        self.last_adaptation = datetime.now()
        
    def create_connection(self, source_id: str, target_id: str, 
                         connection_type: str = 'direct', 
                         initial_weight: float = 0.5) -> str:
        """創建新的神經連接"""
        connection_id = f"{source_id}->{target_id}"
        
        if connection_id not in self.connections:
            connection = NeuralConnection(
                source_id=source_id,
                target_id=target_id,
                weight=initial_weight,
                connection_type=connection_type,
                created_time=datetime.now(),
                last_used=datetime.now(),
                metrics=ConnectionMetrics()
            )
            
            self.connections[connection_id] = connection
            logger.info(f"🔗 創建新連接: {connection_id} (權重: {initial_weight:.2f})")
            
        return connection_id
    
    def record_interaction(self, source_id: str, target_id: str, 
                          success: bool, response_time: float = 0.0):
        """記錄神經元間的交互結果"""
        connection_id = f"{source_id}->{target_id}"
        
        # 如果連接不存在，自動創建
        if connection_id not in self.connections:
            self.create_connection(source_id, target_id)
        
        connection = self.connections[connection_id]
        metrics = connection.metrics
        
        # 更新指標
        metrics.total_attempts += 1
        metrics.total_response_time += response_time
        connection.last_used = datetime.now()
        
        if success:
            metrics.successful_attempts += 1
            metrics.last_success_time = datetime.now()
            metrics.consecutive_successes += 1
            metrics.consecutive_failures = 0
            
            # 強化連接
            self.reinforce_connection(connection_id, response_time)
            
        else:
            metrics.failed_attempts += 1
            metrics.last_failure_time = datetime.now()
            metrics.consecutive_failures += 1
            metrics.consecutive_successes = 0
            
            # 弱化連接
            self.weaken_connection(connection_id)
        
        logger.debug(f"📊 記錄交互: {connection_id} - 成功: {success}, 響應時間: {response_time:.3f}s")
    
    def reinforce_connection(self, connection_id: str, response_time: float = 0.0):
        """強化連接權重"""
        if connection_id not in self.connections:
            return
        
        connection = self.connections[connection_id]
        
        # 計算強化因子
        success_rate = self.calculate_success_rate(connection_id)
        avg_response_time = self.calculate_avg_response_time(connection_id)
        
        # 響應時間越短，強化越多
        time_factor = max(0.1, 1.0 - (response_time / 10.0))  # 假設10秒為最大可接受時間
        
        # 成功率越高，強化越多
        success_factor = success_rate
        
        # 計算總強化因子
        reinforcement_factor = (time_factor + success_factor) / 2
        
        # 應用強化
        weight_increase = self.learning_rate * reinforcement_factor
        new_weight = min(connection.weight + weight_increase, self.max_weight)
        
        old_weight = connection.weight
        connection.weight = new_weight
        
        logger.debug(f"💪 強化連接: {connection_id} - 權重: {old_weight:.3f} -> {new_weight:.3f}")
        
        # 記錄強化歷史
        self.reinforcement_history.append({
            'connection_id': connection_id,
            'action': 'reinforce',
            'old_weight': old_weight,
            'new_weight': new_weight,
            'factor': reinforcement_factor,
            'timestamp': datetime.now()
        })
    
    def weaken_connection(self, connection_id: str):
        """弱化連接權重"""
        if connection_id not in self.connections:
            return
        
        connection = self.connections[connection_id]
        
        # 計算弱化因子
        failure_rate = 1.0 - self.calculate_success_rate(connection_id)
        consecutive_failures = connection.metrics.consecutive_failures
        
        # 連續失敗越多，弱化越多
        failure_factor = min(1.0, failure_rate + (consecutive_failures * 0.1))
        
        # 應用弱化
        weight_decrease = self.learning_rate * failure_factor
        new_weight = max(connection.weight - weight_decrease, self.min_weight)
        
        old_weight = connection.weight
        connection.weight = new_weight
        
        logger.debug(f"🔻 弱化連接: {connection_id} - 權重: {old_weight:.3f} -> {new_weight:.3f}")
        
        # 如果權重過低，考慮移除連接
        if new_weight <= self.pruning_threshold:
            self.prune_connection(connection_id)
        
        # 記錄弱化歷史
        self.reinforcement_history.append({
            'connection_id': connection_id,
            'action': 'weaken',
            'old_weight': old_weight,
            'new_weight': new_weight,
            'factor': failure_factor,
            'timestamp': datetime.now()
        })
    
    def prune_connection(self, connection_id: str):
        """修剪（移除）低效連接"""
        if connection_id in self.connections:
            connection = self.connections[connection_id]
            connection.is_active = False
            
            logger.info(f"✂️ 修剪連接: {connection_id} (權重過低: {connection.weight:.3f})")
            
            # 記錄修剪歷史
            self.reinforcement_history.append({
                'connection_id': connection_id,
                'action': 'prune',
                'old_weight': connection.weight,
                'new_weight': 0.0,
                'timestamp': datetime.now()
            })
    
    def calculate_success_rate(self, connection_id: str) -> float:
        """計算連接成功率"""
        if connection_id not in self.connections:
            return 0.0
        
        metrics = self.connections[connection_id].metrics
        if metrics.total_attempts == 0:
            return 0.0
        
        return metrics.successful_attempts / metrics.total_attempts
    
    def calculate_avg_response_time(self, connection_id: str) -> float:
        """計算平均響應時間"""
        if connection_id not in self.connections:
            return float('inf')
        
        metrics = self.connections[connection_id].metrics
        if metrics.successful_attempts == 0:
            return float('inf')
        
        return metrics.total_response_time / metrics.successful_attempts
    
    def get_best_connections(self, source_id: str, limit: int = 5) -> List[NeuralConnection]:
        """獲取從指定源神經元出發的最佳連接"""
        source_connections = [
            conn for conn in self.connections.values()
            if conn.source_id == source_id and conn.is_active
        ]
        
        # 按權重排序
        source_connections.sort(key=lambda x: x.weight, reverse=True)
        
        return source_connections[:limit]
    
    def get_connection_score(self, connection_id: str) -> float:
        """計算連接的綜合評分"""
        if connection_id not in self.connections:
            return 0.0
        
        connection = self.connections[connection_id]
        metrics = connection.metrics
        
        # 成功率評分
        success_rate = self.calculate_success_rate(connection_id)
        success_score = success_rate * self.success_rate_weight
        
        # 響應時間評分（越短越好）
        avg_response_time = self.calculate_avg_response_time(connection_id)
        if avg_response_time == float('inf'):
            time_score = 0.0
        else:
            time_score = max(0.0, 1.0 - (avg_response_time / 10.0)) * self.response_time_weight
        
        # 使用頻率評分
        usage_frequency = metrics.total_attempts / max(1, (datetime.now() - connection.created_time).days + 1)
        frequency_score = min(1.0, usage_frequency / 10.0) * self.usage_frequency_weight
        
        total_score = success_score + time_score + frequency_score
        
        return total_score
    
    def apply_weight_decay(self):
        """應用權重衰減，防止過度強化"""
        for connection in self.connections.values():
            if connection.is_active:
                # 計算自上次使用以來的時間
                time_since_use = (datetime.now() - connection.last_used).total_seconds() / 3600  # 小時
                
                # 應用衰減
                decay_factor = math.exp(-self.decay_rate * time_since_use)
                new_weight = connection.weight * decay_factor
                
                # 確保權重不低於最小值
                connection.weight = max(new_weight, self.min_weight)
    
    def adapt_parameters(self):
        """自適應調整強化學習參數"""
        current_time = datetime.now()
        
        if (current_time - self.last_adaptation).total_seconds() < self.adaptation_cycle:
            return
        
        # 分析最近的強化歷史
        recent_history = [
            h for h in self.reinforcement_history
            if (current_time - h['timestamp']).total_seconds() < self.adaptation_cycle
        ]
        
        if len(recent_history) > 10:
            # 計算強化和弱化的比例
            reinforcements = len([h for h in recent_history if h['action'] == 'reinforce'])
            weakenings = len([h for h in recent_history if h['action'] == 'weaken'])
            
            reinforce_ratio = reinforcements / len(recent_history)
            
            # 調整學習率
            if reinforce_ratio > 0.7:
                # 強化過多，降低學習率
                self.learning_rate = max(0.01, self.learning_rate * 0.9)
            elif reinforce_ratio < 0.3:
                # 強化過少，提高學習率
                self.learning_rate = min(0.3, self.learning_rate * 1.1)
            
            logger.info(f"🎯 自適應調整: 學習率={self.learning_rate:.3f}, 強化比例={reinforce_ratio:.2f}")
        
        self.last_adaptation = current_time
    
    def get_network_topology(self) -> Dict:
        """獲取網路拓撲結構"""
        active_connections = [conn for conn in self.connections.values() if conn.is_active]
        
        # 構建節點和邊的信息
        nodes = set()
        edges = []
        
        for conn in active_connections:
            nodes.add(conn.source_id)
            nodes.add(conn.target_id)
            
            edges.append({
                'source': conn.source_id,
                'target': conn.target_id,
                'weight': conn.weight,
                'type': conn.connection_type,
                'score': self.get_connection_score(f"{conn.source_id}->{conn.target_id}")
            })
        
        return {
            'nodes': list(nodes),
            'edges': edges,
            'total_connections': len(active_connections),
            'avg_weight': sum(conn.weight for conn in active_connections) / len(active_connections) if active_connections else 0
        }
    
    def get_reinforcement_stats(self) -> Dict:
        """獲取強化學習統計信息"""
        active_connections = [conn for conn in self.connections.values() if conn.is_active]
        
        if not active_connections:
            return {'message': '沒有活躍連接'}
        
        weights = [conn.weight for conn in active_connections]
        success_rates = [self.calculate_success_rate(f"{conn.source_id}->{conn.target_id}") for conn in active_connections]
        
        return {
            'total_connections': len(self.connections),
            'active_connections': len(active_connections),
            'avg_weight': sum(weights) / len(weights),
            'max_weight': max(weights),
            'min_weight': min(weights),
            'avg_success_rate': sum(success_rates) / len(success_rates),
            'learning_rate': self.learning_rate,
            'reinforcement_events': len(self.reinforcement_history),
            'last_adaptation': self.last_adaptation
        }

# 測試和演示代碼
def test_reinforcement_engine():
    """測試連接強化引擎"""
    engine = ConnectionReinforcementEngine()
    
    # 模擬一些連接和交互
    print("🧪 測試連接強化引擎")
    
    # 創建連接
    engine.create_connection("product_orchestrator", "smartui_mcp")
    engine.create_connection("product_orchestrator", "kilocode_mcp")
    engine.create_connection("smartui_mcp", "kilocode_mcp")
    
    # 模擬成功的交互
    for i in range(10):
        engine.record_interaction("product_orchestrator", "smartui_mcp", True, 0.5)
        engine.record_interaction("product_orchestrator", "kilocode_mcp", True, 1.2)
    
    # 模擬一些失敗的交互
    for i in range(3):
        engine.record_interaction("smartui_mcp", "kilocode_mcp", False, 5.0)
    
    # 顯示統計信息
    stats = engine.get_reinforcement_stats()
    print("\n📊 強化學習統計:")
    print(json.dumps(stats, indent=2, default=str))
    
    # 顯示網路拓撲
    topology = engine.get_network_topology()
    print("\n🕸️ 網路拓撲:")
    print(json.dumps(topology, indent=2))
    
    # 獲取最佳連接
    best_connections = engine.get_best_connections("product_orchestrator")
    print(f"\n🏆 最佳連接 (從 product_orchestrator):")
    for conn in best_connections:
        score = engine.get_connection_score(f"{conn.source_id}->{conn.target_id}")
        print(f"  {conn.target_id}: 權重={conn.weight:.3f}, 評分={score:.3f}")

if __name__ == "__main__":
    test_reinforcement_engine()

