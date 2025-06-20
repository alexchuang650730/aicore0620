#!/usr/bin/env python3
"""
自進化 MCP 神經網路 - 自進化學習器
Self-Evolution Learner for MCP Neural Network

持續學習和優化系統行為，適應新的使用模式
"""

import asyncio
import json
import time
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)

@dataclass
class LearningPattern:
    """學習模式數據結構"""
    pattern_id: str
    pattern_type: str  # 'workflow', 'connection', 'usage', 'performance'
    pattern_data: Dict[str, Any]
    confidence: float
    usage_count: int
    success_rate: float
    discovered_time: datetime
    last_used: datetime

@dataclass
class EvolutionEvent:
    """進化事件數據結構"""
    event_id: str
    event_type: str  # 'adaptation', 'optimization', 'learning', 'pruning'
    source_component: str
    target_component: Optional[str]
    event_data: Dict[str, Any]
    impact_score: float
    timestamp: datetime

class SelfEvolutionLearner:
    """
    自進化學習器
    
    核心功能：
    1. 持續學習系統使用模式
    2. 識別和強化成功模式
    3. 自動適應新的需求
    4. 優化整體系統性能
    """
    
    def __init__(self):
        self.learned_patterns: Dict[str, LearningPattern] = {}
        self.evolution_events: List[EvolutionEvent] = []
        self.behavior_history: deque = deque(maxlen=1000)
        
        # 學習參數
        self.learning_threshold = 0.7
        self.pattern_confidence_threshold = 0.8
        self.adaptation_sensitivity = 0.1
        self.evolution_cycle_interval = 1800  # 30分鐘
        
        # 模式識別參數
        self.min_pattern_occurrences = 5
        self.pattern_similarity_threshold = 0.85
        self.pattern_decay_rate = 0.05
        
        # 自適應參數
        self.performance_window = 100  # 最近100次交互
        self.adaptation_history: deque = deque(maxlen=50)
        
        # 進化狀態
        self.is_learning = False
        self.last_evolution_cycle = datetime.now()
        self.evolution_generation = 0
        
    async def start_learning(self):
        """啟動持續學習過程"""
        self.is_learning = True
        logger.info("🧠 自進化學習器啟動")
        
        while self.is_learning:
            try:
                await self.evolution_cycle()
                await asyncio.sleep(self.evolution_cycle_interval)
            except Exception as e:
                logger.error(f"進化循環錯誤: {e}")
                await asyncio.sleep(60)
    
    async def evolution_cycle(self):
        """單次進化循環"""
        self.evolution_generation += 1
        logger.info(f"🔄 開始進化循環 #{self.evolution_generation}")
        
        # 1. 分析行為模式
        await self.analyze_behavior_patterns()
        
        # 2. 識別新的學習模式
        await self.identify_learning_patterns()
        
        # 3. 優化現有模式
        await self.optimize_existing_patterns()
        
        # 4. 適應性調整
        await self.adaptive_adjustment()
        
        # 5. 清理過時模式
        await self.prune_obsolete_patterns()
        
        # 6. 記錄進化事件
        self.record_evolution_event(
            event_type='evolution_cycle',
            source_component='self_evolution_learner',
            event_data={
                'generation': self.evolution_generation,
                'patterns_count': len(self.learned_patterns),
                'events_count': len(self.evolution_events)
            },
            impact_score=0.5
        )
        
        self.last_evolution_cycle = datetime.now()
        logger.info(f"✅ 進化循環 #{self.evolution_generation} 完成")
    
    def record_behavior(self, behavior_data: Dict[str, Any]):
        """記錄系統行為數據"""
        behavior_entry = {
            'timestamp': datetime.now(),
            'data': behavior_data
        }
        
        self.behavior_history.append(behavior_entry)
        logger.debug(f"📝 記錄行為: {behavior_data.get('action', 'unknown')}")
    
    async def analyze_behavior_patterns(self):
        """分析行為模式"""
        if len(self.behavior_history) < self.min_pattern_occurrences:
            return
        
        logger.info("🔍 分析行為模式")
        
        # 分析工作流模式
        workflow_patterns = self.extract_workflow_patterns()
        
        # 分析連接模式
        connection_patterns = self.extract_connection_patterns()
        
        # 分析使用模式
        usage_patterns = self.extract_usage_patterns()
        
        # 分析性能模式
        performance_patterns = self.extract_performance_patterns()
        
        logger.info(f"📊 發現模式: 工作流={len(workflow_patterns)}, 連接={len(connection_patterns)}, 使用={len(usage_patterns)}, 性能={len(performance_patterns)}")
    
    def extract_workflow_patterns(self) -> List[Dict]:
        """提取工作流模式"""
        workflow_sequences = defaultdict(int)
        
        # 分析最近的行為序列
        recent_behaviors = list(self.behavior_history)[-50:]
        
        for i in range(len(recent_behaviors) - 2):
            sequence = []
            for j in range(3):  # 3步序列
                if i + j < len(recent_behaviors):
                    behavior = recent_behaviors[i + j]['data']
                    if 'workflow' in behavior:
                        sequence.append(behavior['workflow'])
            
            if len(sequence) == 3:
                sequence_key = ' -> '.join(sequence)
                workflow_sequences[sequence_key] += 1
        
        # 識別頻繁模式
        patterns = []
        for sequence, count in workflow_sequences.items():
            if count >= self.min_pattern_occurrences:
                patterns.append({
                    'sequence': sequence,
                    'frequency': count,
                    'confidence': min(1.0, count / 10.0)
                })
        
        return patterns
    
    def extract_connection_patterns(self) -> List[Dict]:
        """提取連接模式"""
        connection_pairs = defaultdict(int)
        
        for behavior in self.behavior_history:
            data = behavior['data']
            if 'source' in data and 'target' in data:
                pair = f"{data['source']} -> {data['target']}"
                connection_pairs[pair] += 1
        
        patterns = []
        for pair, count in connection_pairs.items():
            if count >= self.min_pattern_occurrences:
                patterns.append({
                    'connection': pair,
                    'frequency': count,
                    'confidence': min(1.0, count / 20.0)
                })
        
        return patterns
    
    def extract_usage_patterns(self) -> List[Dict]:
        """提取使用模式"""
        hourly_usage = defaultdict(int)
        component_usage = defaultdict(int)
        
        for behavior in self.behavior_history:
            timestamp = behavior['timestamp']
            hour = timestamp.hour
            hourly_usage[hour] += 1
            
            data = behavior['data']
            if 'component' in data:
                component_usage[data['component']] += 1
        
        patterns = []
        
        # 時間模式
        peak_hours = sorted(hourly_usage.items(), key=lambda x: x[1], reverse=True)[:3]
        if peak_hours:
            patterns.append({
                'type': 'time_pattern',
                'peak_hours': [hour for hour, count in peak_hours],
                'confidence': 0.8
            })
        
        # 組件使用模式
        popular_components = sorted(component_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        if popular_components:
            patterns.append({
                'type': 'component_usage',
                'popular_components': [comp for comp, count in popular_components],
                'confidence': 0.7
            })
        
        return patterns
    
    def extract_performance_patterns(self) -> List[Dict]:
        """提取性能模式"""
        response_times = []
        success_rates = defaultdict(list)
        
        for behavior in self.behavior_history:
            data = behavior['data']
            
            if 'response_time' in data:
                response_times.append(data['response_time'])
            
            if 'component' in data and 'success' in data:
                success_rates[data['component']].append(data['success'])
        
        patterns = []
        
        # 響應時間模式
        if response_times:
            avg_response_time = np.mean(response_times)
            patterns.append({
                'type': 'response_time',
                'avg_time': avg_response_time,
                'trend': 'improving' if len(response_times) > 10 and np.mean(response_times[-10:]) < avg_response_time else 'stable',
                'confidence': 0.6
            })
        
        # 成功率模式
        for component, successes in success_rates.items():
            if len(successes) >= 5:
                success_rate = sum(successes) / len(successes)
                patterns.append({
                    'type': 'success_rate',
                    'component': component,
                    'rate': success_rate,
                    'confidence': min(1.0, len(successes) / 20.0)
                })
        
        return patterns
    
    async def identify_learning_patterns(self):
        """識別新的學習模式"""
        logger.info("🎯 識別學習模式")
        
        # 這裡可以實現更複雜的模式識別算法
        # 例如使用機器學習技術來識別隱藏模式
        
        # 簡化版本：基於頻率和成功率識別模式
        pattern_candidates = self.generate_pattern_candidates()
        
        for candidate in pattern_candidates:
            pattern_id = self.generate_pattern_id(candidate)
            
            if pattern_id not in self.learned_patterns:
                # 創建新的學習模式
                pattern = LearningPattern(
                    pattern_id=pattern_id,
                    pattern_type=candidate['type'],
                    pattern_data=candidate['data'],
                    confidence=candidate['confidence'],
                    usage_count=1,
                    success_rate=candidate.get('success_rate', 0.5),
                    discovered_time=datetime.now(),
                    last_used=datetime.now()
                )
                
                self.learned_patterns[pattern_id] = pattern
                logger.info(f"🆕 發現新模式: {pattern_id}")
                
                # 記錄進化事件
                self.record_evolution_event(
                    event_type='learning',
                    source_component='pattern_identifier',
                    event_data={'pattern_id': pattern_id, 'pattern_type': candidate['type']},
                    impact_score=candidate['confidence']
                )
    
    def generate_pattern_candidates(self) -> List[Dict]:
        """生成模式候選"""
        candidates = []
        
        # 基於最近行為生成候選模式
        recent_behaviors = list(self.behavior_history)[-20:]
        
        # 工作流序列候選
        for i in range(len(recent_behaviors) - 1):
            current = recent_behaviors[i]['data']
            next_behavior = recent_behaviors[i + 1]['data']
            
            if 'workflow' in current and 'workflow' in next_behavior:
                candidates.append({
                    'type': 'workflow_sequence',
                    'data': {
                        'from': current['workflow'],
                        'to': next_behavior['workflow']
                    },
                    'confidence': 0.6,
                    'success_rate': 0.7
                })
        
        return candidates
    
    def generate_pattern_id(self, candidate: Dict) -> str:
        """生成模式ID"""
        pattern_type = candidate['type']
        data_str = json.dumps(candidate['data'], sort_keys=True)
        return f"{pattern_type}_{hash(data_str) % 10000:04d}"
    
    async def optimize_existing_patterns(self):
        """優化現有模式"""
        logger.info("⚡ 優化現有模式")
        
        for pattern_id, pattern in self.learned_patterns.items():
            # 更新模式信心度
            self.update_pattern_confidence(pattern)
            
            # 應用模式衰減
            self.apply_pattern_decay(pattern)
            
            # 檢查模式有效性
            if pattern.confidence < self.pattern_confidence_threshold * 0.5:
                logger.info(f"🗑️ 標記過時模式: {pattern_id}")
                pattern.confidence = 0.0  # 標記為待刪除
    
    def update_pattern_confidence(self, pattern: LearningPattern):
        """更新模式信心度"""
        # 基於使用頻率和成功率更新信心度
        usage_factor = min(1.0, pattern.usage_count / 50.0)
        success_factor = pattern.success_rate
        time_factor = max(0.1, 1.0 - (datetime.now() - pattern.last_used).days / 30.0)
        
        new_confidence = (usage_factor + success_factor + time_factor) / 3.0
        pattern.confidence = new_confidence
    
    def apply_pattern_decay(self, pattern: LearningPattern):
        """應用模式衰減"""
        days_since_use = (datetime.now() - pattern.last_used).days
        decay_factor = max(0.1, 1.0 - (days_since_use * self.pattern_decay_rate))
        pattern.confidence *= decay_factor
    
    async def adaptive_adjustment(self):
        """適應性調整"""
        logger.info("🔧 適應性調整")
        
        # 分析系統性能趨勢
        performance_trend = self.analyze_performance_trend()
        
        # 根據趨勢調整參數
        if performance_trend == 'declining':
            # 性能下降，增加學習敏感度
            self.adaptation_sensitivity = min(0.3, self.adaptation_sensitivity * 1.2)
            logger.info("📈 增加學習敏感度")
        elif performance_trend == 'improving':
            # 性能改善，可以降低敏感度
            self.adaptation_sensitivity = max(0.05, self.adaptation_sensitivity * 0.9)
            logger.info("📉 降低學習敏感度")
        
        # 記錄適應性調整
        self.adaptation_history.append({
            'timestamp': datetime.now(),
            'trend': performance_trend,
            'sensitivity': self.adaptation_sensitivity
        })
    
    def analyze_performance_trend(self) -> str:
        """分析性能趨勢"""
        if len(self.behavior_history) < 20:
            return 'stable'
        
        recent_behaviors = list(self.behavior_history)[-20:]
        older_behaviors = list(self.behavior_history)[-40:-20] if len(self.behavior_history) >= 40 else []
        
        if not older_behaviors:
            return 'stable'
        
        # 計算平均響應時間
        recent_times = [b['data'].get('response_time', 1.0) for b in recent_behaviors if 'response_time' in b['data']]
        older_times = [b['data'].get('response_time', 1.0) for b in older_behaviors if 'response_time' in b['data']]
        
        if not recent_times or not older_times:
            return 'stable'
        
        recent_avg = np.mean(recent_times)
        older_avg = np.mean(older_times)
        
        if recent_avg < older_avg * 0.9:
            return 'improving'
        elif recent_avg > older_avg * 1.1:
            return 'declining'
        else:
            return 'stable'
    
    async def prune_obsolete_patterns(self):
        """清理過時模式"""
        obsolete_patterns = [
            pattern_id for pattern_id, pattern in self.learned_patterns.items()
            if pattern.confidence <= 0.0
        ]
        
        for pattern_id in obsolete_patterns:
            del self.learned_patterns[pattern_id]
            logger.info(f"🗑️ 移除過時模式: {pattern_id}")
            
            # 記錄清理事件
            self.record_evolution_event(
                event_type='pruning',
                source_component='pattern_pruner',
                event_data={'pattern_id': pattern_id},
                impact_score=0.2
            )
    
    def record_evolution_event(self, event_type: str, source_component: str, 
                             event_data: Dict[str, Any], impact_score: float,
                             target_component: Optional[str] = None):
        """記錄進化事件"""
        event = EvolutionEvent(
            event_id=f"{event_type}_{int(time.time())}_{len(self.evolution_events)}",
            event_type=event_type,
            source_component=source_component,
            target_component=target_component,
            event_data=event_data,
            impact_score=impact_score,
            timestamp=datetime.now()
        )
        
        self.evolution_events.append(event)
        
        # 保持事件歷史在合理範圍內
        if len(self.evolution_events) > 1000:
            self.evolution_events = self.evolution_events[-500:]
    
    def get_learning_stats(self) -> Dict:
        """獲取學習統計信息"""
        active_patterns = [p for p in self.learned_patterns.values() if p.confidence > 0.1]
        
        return {
            'evolution_generation': self.evolution_generation,
            'total_patterns': len(self.learned_patterns),
            'active_patterns': len(active_patterns),
            'behavior_history_size': len(self.behavior_history),
            'evolution_events': len(self.evolution_events),
            'adaptation_sensitivity': self.adaptation_sensitivity,
            'last_evolution_cycle': self.last_evolution_cycle,
            'avg_pattern_confidence': np.mean([p.confidence for p in active_patterns]) if active_patterns else 0.0
        }
    
    def get_top_patterns(self, limit: int = 10) -> List[LearningPattern]:
        """獲取最佳學習模式"""
        active_patterns = [p for p in self.learned_patterns.values() if p.confidence > 0.1]
        active_patterns.sort(key=lambda x: x.confidence * x.success_rate, reverse=True)
        return active_patterns[:limit]
    
    def stop_learning(self):
        """停止學習過程"""
        self.is_learning = False
        logger.info("🛑 自進化學習器停止")

# 測試和演示代碼
def test_evolution_learner():
    """測試自進化學習器"""
    learner = SelfEvolutionLearner()
    
    print("🧪 測試自進化學習器")
    
    # 模擬一些行為數據
    behaviors = [
        {'action': 'workflow_start', 'workflow': 'smartui_development', 'component': 'product_orchestrator', 'response_time': 0.5, 'success': True},
        {'action': 'mcp_call', 'source': 'product_orchestrator', 'target': 'smartui_mcp', 'response_time': 1.2, 'success': True},
        {'action': 'mcp_call', 'source': 'smartui_mcp', 'target': 'kilocode_mcp', 'response_time': 2.1, 'success': True},
        {'action': 'workflow_complete', 'workflow': 'smartui_development', 'component': 'product_orchestrator', 'response_time': 0.3, 'success': True},
    ]
    
    # 記錄多次行為
    for _ in range(10):
        for behavior in behaviors:
            learner.record_behavior(behavior)
    
    # 執行一次進化循環
    import asyncio
    asyncio.run(learner.evolution_cycle())
    
    # 顯示學習統計
    stats = learner.get_learning_stats()
    print("\n📊 學習統計:")
    print(json.dumps(stats, indent=2, default=str))
    
    # 顯示最佳模式
    top_patterns = learner.get_top_patterns(5)
    print(f"\n🏆 最佳學習模式 ({len(top_patterns)}):")
    for pattern in top_patterns:
        print(f"  {pattern.pattern_id}: 信心度={pattern.confidence:.3f}, 成功率={pattern.success_rate:.3f}")

if __name__ == "__main__":
    test_evolution_learner()

