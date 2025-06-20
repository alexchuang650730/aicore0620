#!/usr/bin/env python3
"""
動態領域知識庫系統
支持配置化、可學習、可擴展的領域知識管理
"""

import json
import yaml
import os
import re
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from pathlib import Path
import jieba
import jieba.posseg as pseg
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)

@dataclass
class DomainFeature:
    """領域特徵"""
    keywords: List[str]
    processes: List[str]
    metrics: List[str]
    entities: List[str]
    patterns: List[str]
    confidence: float = 0.0

@dataclass
class DomainProfile:
    """領域檔案"""
    name: str
    description: str
    features: DomainFeature
    parent_domain: Optional[str] = None
    sub_domains: List[str] = None
    learning_enabled: bool = True

class DynamicDomainKnowledge:
    """動態領域知識庫"""
    
    def __init__(self, config_dir: str = "domain_configs"):
        self.config_dir = Path(config_dir)
        self.domains: Dict[str, DomainProfile] = {}
        self.learned_patterns: Dict[str, Set[str]] = defaultdict(set)
        self.domain_statistics: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        
        # 確保配置目錄存在
        self.config_dir.mkdir(exist_ok=True)
        
        # 加載預設領域配置
        self._load_domain_configs()
        
        # 初始化動態學習組件
        self._init_learning_components()
    
    def _load_domain_configs(self):
        """加載領域配置文件"""
        
        # 如果沒有配置文件，創建基礎配置
        if not any(self.config_dir.glob("*.yaml")) and not any(self.config_dir.glob("*.json")):
            self._create_default_configs()
        
        # 加載所有配置文件
        for config_file in self.config_dir.glob("*.yaml"):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    self._register_domain_from_config(config)
            except Exception as e:
                logger.error(f"加載領域配置失敗 {config_file}: {e}")
        
        for config_file in self.config_dir.glob("*.json"):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self._register_domain_from_config(config)
            except Exception as e:
                logger.error(f"加載領域配置失敗 {config_file}: {e}")
    
    def _create_default_configs(self):
        """創建預設領域配置"""
        
        # 保險領域配置
        insurance_config = {
            "name": "insurance",
            "description": "保險業務領域",
            "features": {
                "keywords": ["保險", "核保", "理賠", "保單", "承保", "風險", "保費"],
                "processes": ["核保流程", "理賠流程", "承保流程", "風險評估", "保單管理"],
                "metrics": ["保費", "賠付率", "承保率", "風險係數", "保額"],
                "entities": ["被保險人", "受益人", "保險公司", "代理人", "核保員"],
                "patterns": [
                    r"保險.*流程",
                    r"核保.*標準",
                    r"理賠.*程序",
                    r"\d+%.*賠付",
                    r"風險.*評估"
                ]
            },
            "sub_domains": ["life_insurance", "property_insurance", "health_insurance"],
            "learning_enabled": True
        }
        
        # 電商領域配置
        ecommerce_config = {
            "name": "ecommerce",
            "description": "電子商務領域",
            "features": {
                "keywords": ["電商", "購物", "訂單", "支付", "物流", "庫存", "客戶"],
                "processes": ["下單流程", "支付流程", "物流流程", "退貨流程", "客服流程"],
                "metrics": ["轉換率", "客單價", "復購率", "庫存周轉率", "滿意度"],
                "entities": ["買家", "賣家", "商品", "訂單", "快遞"],
                "patterns": [
                    r"購物.*流程",
                    r"訂單.*管理",
                    r"支付.*系統",
                    r"\d+%.*轉換率",
                    r"庫存.*管理"
                ]
            },
            "learning_enabled": True
        }
        
        # 金融領域配置
        finance_config = {
            "name": "finance",
            "description": "金融服務領域",
            "features": {
                "keywords": ["金融", "銀行", "貸款", "投資", "風控", "合規", "資金"],
                "processes": ["放貸流程", "風控流程", "合規流程", "投資流程", "清算流程"],
                "metrics": ["利率", "風險係數", "資本充足率", "不良率", "收益率"],
                "entities": ["借款人", "投資者", "銀行", "監管機構", "評級機構"],
                "patterns": [
                    r"風險.*控制",
                    r"合規.*要求",
                    r"資金.*管理",
                    r"\d+%.*利率",
                    r"信用.*評估"
                ]
            },
            "learning_enabled": True
        }
        
        # 保存配置文件
        configs = [
            (insurance_config, "insurance.yaml"),
            (ecommerce_config, "ecommerce.yaml"),
            (finance_config, "finance.yaml")
        ]
        
        for config, filename in configs:
            config_path = self.config_dir / filename
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    def _register_domain_from_config(self, config: Dict[str, Any]):
        """從配置註冊領域"""
        try:
            features = DomainFeature(**config["features"])
            domain = DomainProfile(
                name=config["name"],
                description=config["description"],
                features=features,
                parent_domain=config.get("parent_domain"),
                sub_domains=config.get("sub_domains", []),
                learning_enabled=config.get("learning_enabled", True)
            )
            self.domains[domain.name] = domain
            logger.info(f"註冊領域: {domain.name}")
        except Exception as e:
            logger.error(f"註冊領域失敗: {e}")
    
    def _init_learning_components(self):
        """初始化學習組件"""
        self.keyword_extractor = KeywordExtractor()
        self.pattern_learner = PatternLearner()
        self.domain_classifier = DomainClassifier(self.domains)
    
    def detect_domain(self, text: str) -> str:
        """檢測文本領域"""
        
        # 使用分類器進行領域檢測
        domain_scores = self.domain_classifier.classify(text)
        
        # 如果沒有明確的領域匹配，嘗試動態學習
        if not domain_scores or max(domain_scores.values()) < 0.3:
            learned_domain = self._learn_from_text(text)
            if learned_domain:
                return learned_domain
        
        # 返回最高分數的領域
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        
        return "general"
    
    def _learn_from_text(self, text: str) -> Optional[str]:
        """從文本中學習新的領域特徵"""
        
        # 提取關鍵詞
        keywords = self.keyword_extractor.extract(text)
        
        # 提取模式
        patterns = self.pattern_learner.extract(text)
        
        # 嘗試匹配現有領域並更新
        for domain_name, domain in self.domains.items():
            if not domain.learning_enabled:
                continue
            
            # 計算相似度
            similarity = self._calculate_similarity(keywords, patterns, domain)
            
            if similarity > 0.5:  # 相似度閾值
                # 更新領域特徵
                self._update_domain_features(domain_name, keywords, patterns)
                return domain_name
        
        # 如果沒有匹配的領域，考慮創建新領域
        if len(keywords) > 5:  # 足夠的關鍵詞
            new_domain_name = self._suggest_new_domain(keywords, patterns)
            if new_domain_name:
                return new_domain_name
        
        return None
    
    def _calculate_similarity(self, keywords: List[str], patterns: List[str], domain: DomainProfile) -> float:
        """計算與現有領域的相似度"""
        
        keyword_overlap = len(set(keywords) & set(domain.features.keywords))
        keyword_similarity = keyword_overlap / max(len(keywords), len(domain.features.keywords), 1)
        
        # 簡化的相似度計算
        return keyword_similarity
    
    def _update_domain_features(self, domain_name: str, keywords: List[str], patterns: List[str]):
        """更新領域特徵"""
        
        domain = self.domains[domain_name]
        
        # 添加新關鍵詞（去重）
        existing_keywords = set(domain.features.keywords)
        new_keywords = [kw for kw in keywords if kw not in existing_keywords]
        domain.features.keywords.extend(new_keywords[:5])  # 限制數量
        
        # 更新學習統計
        self.domain_statistics[domain_name]["learned_keywords"] += len(new_keywords)
        self.domain_statistics[domain_name]["total_updates"] += 1
        
        logger.info(f"更新領域 {domain_name}: 新增 {len(new_keywords)} 個關鍵詞")
    
    def _suggest_new_domain(self, keywords: List[str], patterns: List[str]) -> Optional[str]:
        """建議新領域"""
        
        # 基於關鍵詞聚類建議新領域名稱
        # 這裡可以實現更複雜的邏輯
        
        if any("醫療" in kw or "健康" in kw for kw in keywords):
            return "healthcare"
        elif any("教育" in kw or "學習" in kw for kw in keywords):
            return "education"
        elif any("製造" in kw or "生產" in kw for kw in keywords):
            return "manufacturing"
        
        return None
    
    def get_domain_features(self, domain_name: str) -> Optional[DomainFeature]:
        """獲取領域特徵"""
        domain = self.domains.get(domain_name)
        return domain.features if domain else None
    
    def add_custom_domain(self, domain_config: Dict[str, Any]) -> bool:
        """添加自定義領域"""
        try:
            self._register_domain_from_config(domain_config)
            
            # 保存到配置文件
            config_file = self.config_dir / f"{domain_config['name']}.yaml"
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(domain_config, f, default_flow_style=False, allow_unicode=True)
            
            return True
        except Exception as e:
            logger.error(f"添加自定義領域失敗: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """獲取學習統計"""
        return {
            "total_domains": len(self.domains),
            "learning_enabled_domains": sum(1 for d in self.domains.values() if d.learning_enabled),
            "domain_statistics": dict(self.domain_statistics),
            "domains": {name: {
                "keywords_count": len(domain.features.keywords),
                "processes_count": len(domain.features.processes),
                "metrics_count": len(domain.features.metrics)
            } for name, domain in self.domains.items()}
        }

class KeywordExtractor:
    """關鍵詞提取器"""
    
    def extract(self, text: str) -> List[str]:
        """提取關鍵詞"""
        
        # 使用jieba進行分詞和詞性標註
        words = pseg.cut(text)
        
        keywords = []
        for word, flag in words:
            # 過濾有意義的詞性
            if (flag.startswith('n') or flag.startswith('v') or flag.startswith('a')) and len(word) > 1:
                keywords.append(word)
        
        # 統計詞頻並返回高頻詞
        word_freq = Counter(keywords)
        return [word for word, freq in word_freq.most_common(20)]

class PatternLearner:
    """模式學習器"""
    
    def extract(self, text: str) -> List[str]:
        """提取文本模式"""
        
        patterns = []
        
        # 提取數字+單位模式
        number_patterns = re.findall(r'\d+(?:\.\d+)?[%元人件天月年]', text)
        patterns.extend(number_patterns)
        
        # 提取流程模式
        process_patterns = re.findall(r'\w+流程|\w+程序|\w+步驟', text)
        patterns.extend(process_patterns)
        
        # 提取管理模式
        management_patterns = re.findall(r'\w+管理|\w+控制|\w+監督', text)
        patterns.extend(management_patterns)
        
        return patterns

class DomainClassifier:
    """領域分類器"""
    
    def __init__(self, domains: Dict[str, DomainProfile]):
        self.domains = domains
    
    def classify(self, text: str) -> Dict[str, float]:
        """分類文本到領域"""
        
        scores = {}
        
        for domain_name, domain in self.domains.items():
            score = self._calculate_domain_score(text, domain)
            if score > 0:
                scores[domain_name] = score
        
        return scores
    
    def _calculate_domain_score(self, text: str, domain: DomainProfile) -> float:
        """計算領域分數"""
        
        total_score = 0.0
        
        # 關鍵詞匹配分數
        keyword_matches = sum(1 for keyword in domain.features.keywords if keyword in text)
        keyword_score = keyword_matches / max(len(domain.features.keywords), 1)
        total_score += keyword_score * 0.4
        
        # 流程匹配分數
        process_matches = sum(1 for process in domain.features.processes if process in text)
        process_score = process_matches / max(len(domain.features.processes), 1)
        total_score += process_score * 0.3
        
        # 模式匹配分數
        pattern_matches = 0
        for pattern in domain.features.patterns:
            if re.search(pattern, text):
                pattern_matches += 1
        pattern_score = pattern_matches / max(len(domain.features.patterns), 1)
        total_score += pattern_score * 0.3
        
        return total_score

# 全局動態領域知識庫實例
dynamic_domain_knowledge = DynamicDomainKnowledge()

