#!/usr/bin/env python3
"""
Incremental Engine
增量引擎 - 提供增量分析、版本比較和智能更新能力
"""

import asyncio
import json
import uuid
import hashlib
from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime
from enum import Enum
import logging
from dataclasses import dataclass, asdict
import difflib

class ChangeType(Enum):
    """變更類型"""
    ADDITION = "addition"
    MODIFICATION = "modification"
    DELETION = "deletion"
    RESTRUCTURE = "restructure"
    ENHANCEMENT = "enhancement"

class ImpactLevel(Enum):
    """影響級別"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class VersionInfo:
    """版本信息"""
    version_id: str
    timestamp: datetime
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    checksum: str

@dataclass
class ChangeRecord:
    """變更記錄"""
    change_id: str
    change_type: ChangeType
    component: str
    old_value: Any
    new_value: Any
    impact_level: ImpactLevel
    description: str
    affected_components: List[str]
    effort_impact: float  # 工作量影響百分比

@dataclass
class IncrementalAnalysis:
    """增量分析結果"""
    analysis_id: str
    from_version: str
    to_version: str
    changes: List[ChangeRecord]
    overall_impact: ImpactLevel
    effort_delta: float
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    timestamp: datetime

class IncrementalEngine:
    """
    增量引擎
    提供智能的增量分析、版本比較和變更影響評估
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "IncrementalEngine"
        self.config = config or {}
        self.versions: Dict[str, VersionInfo] = {}
        self.analyses: Dict[str, IncrementalAnalysis] = {}
        self.change_patterns: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger(self.name)
        
        # 變更檢測規則
        self.detection_rules = {
            "functional_requirements": {
                "weight": 0.8,
                "impact_multiplier": 1.5,
                "keywords": ["功能", "需求", "特性", "接口"]
            },
            "non_functional_requirements": {
                "weight": 0.6,
                "impact_multiplier": 1.2,
                "keywords": ["性能", "安全", "可用性", "擴展性"]
            },
            "technical_constraints": {
                "weight": 0.7,
                "impact_multiplier": 1.3,
                "keywords": ["技術", "架構", "平台", "工具"]
            },
            "business_rules": {
                "weight": 0.9,
                "impact_multiplier": 1.6,
                "keywords": ["業務", "規則", "流程", "邏輯"]
            }
        }
        
        # 影響評估矩陣
        self.impact_matrix = {
            "addition": {"base_impact": 0.3, "complexity_factor": 1.2},
            "modification": {"base_impact": 0.5, "complexity_factor": 1.5},
            "deletion": {"base_impact": 0.4, "complexity_factor": 1.1},
            "restructure": {"base_impact": 0.8, "complexity_factor": 2.0},
            "enhancement": {"base_impact": 0.6, "complexity_factor": 1.3}
        }
    
    def create_version(self, content: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> str:
        """創建新版本"""
        version_id = str(uuid.uuid4())
        content_str = json.dumps(content, sort_keys=True, ensure_ascii=False)
        checksum = hashlib.sha256(content_str.encode()).hexdigest()
        
        version = VersionInfo(
            version_id=version_id,
            timestamp=datetime.now(),
            content=content,
            metadata=metadata or {},
            checksum=checksum
        )
        
        self.versions[version_id] = version
        self.logger.info(f"版本已創建: {version_id}")
        
        return version_id
    
    async def analyze_incremental_changes(self, from_version_id: str, to_version_id: str) -> IncrementalAnalysis:
        """分析增量變更"""
        if from_version_id not in self.versions:
            raise ValueError(f"源版本 {from_version_id} 不存在")
        if to_version_id not in self.versions:
            raise ValueError(f"目標版本 {to_version_id} 不存在")
        
        from_version = self.versions[from_version_id]
        to_version = self.versions[to_version_id]
        
        # 檢測變更
        changes = await self._detect_changes(from_version.content, to_version.content)
        
        # 評估影響
        overall_impact = self._assess_overall_impact(changes)
        effort_delta = self._calculate_effort_delta(changes)
        risk_assessment = await self._assess_risks(changes)
        recommendations = self._generate_recommendations(changes)
        
        # 創建分析結果
        analysis = IncrementalAnalysis(
            analysis_id=str(uuid.uuid4()),
            from_version=from_version_id,
            to_version=to_version_id,
            changes=changes,
            overall_impact=overall_impact,
            effort_delta=effort_delta,
            risk_assessment=risk_assessment,
            recommendations=recommendations,
            timestamp=datetime.now()
        )
        
        self.analyses[analysis.analysis_id] = analysis
        return analysis
    
    async def _detect_changes(self, old_content: Dict[str, Any], new_content: Dict[str, Any]) -> List[ChangeRecord]:
        """檢測變更"""
        changes = []
        
        # 檢測結構變更
        old_keys = set(old_content.keys())
        new_keys = set(new_content.keys())
        
        # 新增的鍵
        for key in new_keys - old_keys:
            change = ChangeRecord(
                change_id=str(uuid.uuid4()),
                change_type=ChangeType.ADDITION,
                component=key,
                old_value=None,
                new_value=new_content[key],
                impact_level=self._assess_change_impact(ChangeType.ADDITION, key, None, new_content[key]),
                description=f"新增組件: {key}",
                affected_components=self._find_affected_components(key, new_content),
                effort_impact=self._calculate_effort_impact(ChangeType.ADDITION, key, None, new_content[key])
            )
            changes.append(change)
        
        # 刪除的鍵
        for key in old_keys - new_keys:
            change = ChangeRecord(
                change_id=str(uuid.uuid4()),
                change_type=ChangeType.DELETION,
                component=key,
                old_value=old_content[key],
                new_value=None,
                impact_level=self._assess_change_impact(ChangeType.DELETION, key, old_content[key], None),
                description=f"刪除組件: {key}",
                affected_components=self._find_affected_components(key, old_content),
                effort_impact=self._calculate_effort_impact(ChangeType.DELETION, key, old_content[key], None)
            )
            changes.append(change)
        
        # 修改的鍵
        for key in old_keys & new_keys:
            if old_content[key] != new_content[key]:
                change_type = self._determine_change_type(old_content[key], new_content[key])
                change = ChangeRecord(
                    change_id=str(uuid.uuid4()),
                    change_type=change_type,
                    component=key,
                    old_value=old_content[key],
                    new_value=new_content[key],
                    impact_level=self._assess_change_impact(change_type, key, old_content[key], new_content[key]),
                    description=f"修改組件: {key}",
                    affected_components=self._find_affected_components(key, new_content),
                    effort_impact=self._calculate_effort_impact(change_type, key, old_content[key], new_content[key])
                )
                changes.append(change)
        
        return changes
    
    def _determine_change_type(self, old_value: Any, new_value: Any) -> ChangeType:
        """確定變更類型"""
        if isinstance(old_value, dict) and isinstance(new_value, dict):
            old_keys = set(old_value.keys())
            new_keys = set(new_value.keys())
            
            # 如果結構發生重大變化
            if len(old_keys.symmetric_difference(new_keys)) > len(old_keys) * 0.5:
                return ChangeType.RESTRUCTURE
            else:
                return ChangeType.MODIFICATION
        elif isinstance(old_value, list) and isinstance(new_value, list):
            if len(new_value) > len(old_value):
                return ChangeType.ENHANCEMENT
            else:
                return ChangeType.MODIFICATION
        else:
            return ChangeType.MODIFICATION
    
    def _assess_change_impact(self, change_type: ChangeType, component: str, old_value: Any, new_value: Any) -> ImpactLevel:
        """評估變更影響"""
        base_impact = self.impact_matrix[change_type.value]["base_impact"]
        
        # 根據組件類型調整影響
        component_weight = 0.5
        for rule_name, rule in self.detection_rules.items():
            if any(keyword in component.lower() for keyword in rule["keywords"]):
                component_weight = rule["weight"]
                break
        
        # 計算最終影響分數
        impact_score = base_impact * component_weight
        
        if impact_score >= 0.8:
            return ImpactLevel.CRITICAL
        elif impact_score >= 0.6:
            return ImpactLevel.HIGH
        elif impact_score >= 0.4:
            return ImpactLevel.MEDIUM
        else:
            return ImpactLevel.LOW
    
    def _calculate_effort_impact(self, change_type: ChangeType, component: str, old_value: Any, new_value: Any) -> float:
        """計算工作量影響"""
        base_effort = self.impact_matrix[change_type.value]["base_impact"]
        complexity_factor = self.impact_matrix[change_type.value]["complexity_factor"]
        
        # 根據內容複雜度調整
        complexity_score = self._assess_complexity(new_value if new_value is not None else old_value)
        
        return base_effort * complexity_factor * complexity_score
    
    def _assess_complexity(self, value: Any) -> float:
        """評估內容複雜度"""
        if isinstance(value, dict):
            return min(len(value) * 0.1 + 0.5, 2.0)
        elif isinstance(value, list):
            return min(len(value) * 0.05 + 0.3, 1.5)
        elif isinstance(value, str):
            return min(len(value) * 0.001 + 0.2, 1.2)
        else:
            return 0.5
    
    def _find_affected_components(self, component: str, content: Dict[str, Any]) -> List[str]:
        """查找受影響的組件"""
        affected = []
        
        # 簡單的依賴檢測邏輯
        for key, value in content.items():
            if key != component:
                if isinstance(value, str) and component in value:
                    affected.append(key)
                elif isinstance(value, dict) and component in str(value):
                    affected.append(key)
        
        return affected
    
    def _assess_overall_impact(self, changes: List[ChangeRecord]) -> ImpactLevel:
        """評估整體影響"""
        if not changes:
            return ImpactLevel.LOW
        
        impact_scores = {
            ImpactLevel.LOW: 1,
            ImpactLevel.MEDIUM: 2,
            ImpactLevel.HIGH: 3,
            ImpactLevel.CRITICAL: 4
        }
        
        total_score = sum(impact_scores[change.impact_level] for change in changes)
        average_score = total_score / len(changes)
        
        if average_score >= 3.5:
            return ImpactLevel.CRITICAL
        elif average_score >= 2.5:
            return ImpactLevel.HIGH
        elif average_score >= 1.5:
            return ImpactLevel.MEDIUM
        else:
            return ImpactLevel.LOW
    
    def _calculate_effort_delta(self, changes: List[ChangeRecord]) -> float:
        """計算工作量變化"""
        return sum(change.effort_impact for change in changes)
    
    async def _assess_risks(self, changes: List[ChangeRecord]) -> Dict[str, Any]:
        """評估風險"""
        risks = {
            "technical_risk": 0.0,
            "business_risk": 0.0,
            "timeline_risk": 0.0,
            "integration_risk": 0.0
        }
        
        for change in changes:
            # 技術風險
            if change.change_type in [ChangeType.RESTRUCTURE, ChangeType.MODIFICATION]:
                risks["technical_risk"] += 0.2
            
            # 業務風險
            if "業務" in change.description or "流程" in change.description:
                risks["business_risk"] += 0.3
            
            # 時間風險
            if change.impact_level in [ImpactLevel.HIGH, ImpactLevel.CRITICAL]:
                risks["timeline_risk"] += 0.25
            
            # 集成風險
            if len(change.affected_components) > 2:
                risks["integration_risk"] += 0.15
        
        # 標準化風險分數
        for risk_type in risks:
            risks[risk_type] = min(risks[risk_type], 1.0)
        
        risks["overall_risk"] = sum(risks.values()) / len(risks)
        
        return risks
    
    def _generate_recommendations(self, changes: List[ChangeRecord]) -> List[str]:
        """生成建議"""
        recommendations = []
        
        high_impact_changes = [c for c in changes if c.impact_level in [ImpactLevel.HIGH, ImpactLevel.CRITICAL]]
        if high_impact_changes:
            recommendations.append("建議分階段實施高影響變更，降低風險")
        
        restructure_changes = [c for c in changes if c.change_type == ChangeType.RESTRUCTURE]
        if restructure_changes:
            recommendations.append("結構性變更需要額外的架構評審和測試")
        
        if len(changes) > 10:
            recommendations.append("變更數量較多，建議進行詳細的影響分析")
        
        total_effort = sum(c.effort_impact for c in changes)
        if total_effort > 1.0:
            recommendations.append(f"預計工作量增加 {total_effort*100:.1f}%，需要調整項目計劃")
        
        return recommendations
    
    def get_version_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """獲取版本歷史"""
        sorted_versions = sorted(
            self.versions.values(),
            key=lambda v: v.timestamp,
            reverse=True
        )
        
        return [
            {
                "version_id": v.version_id,
                "timestamp": v.timestamp.isoformat(),
                "checksum": v.checksum[:8],
                "metadata": v.metadata
            }
            for v in sorted_versions[:limit]
        ]
    
    def get_analysis_summary(self, analysis_id: str) -> Dict[str, Any]:
        """獲取分析摘要"""
        if analysis_id not in self.analyses:
            raise ValueError(f"分析 {analysis_id} 不存在")
        
        analysis = self.analyses[analysis_id]
        
        return {
            "analysis_id": analysis.analysis_id,
            "from_version": analysis.from_version,
            "to_version": analysis.to_version,
            "total_changes": len(analysis.changes),
            "changes_by_type": {
                change_type.value: len([c for c in analysis.changes if c.change_type == change_type])
                for change_type in ChangeType
            },
            "overall_impact": analysis.overall_impact.value,
            "effort_delta": analysis.effort_delta,
            "risk_assessment": analysis.risk_assessment,
            "recommendations": analysis.recommendations,
            "timestamp": analysis.timestamp.isoformat()
        }
    
    def get_engine_status(self) -> Dict[str, Any]:
        """獲取引擎狀態"""
        return {
            "name": self.name,
            "total_versions": len(self.versions),
            "total_analyses": len(self.analyses),
            "recent_versions": [v.version_id for v in sorted(self.versions.values(), key=lambda x: x.timestamp, reverse=True)[:5]],
            "recent_analyses": [a.analysis_id for a in sorted(self.analyses.values(), key=lambda x: x.timestamp, reverse=True)[:5]],
            "detection_rules": list(self.detection_rules.keys())
        }

