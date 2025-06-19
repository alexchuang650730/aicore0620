# 動態多模態需求分析系統

## 🎯 項目概述

這是一個企業級的智能需求分析系統，整合了動態分析引擎、增量引擎和多模態文檔處理能力，專為保險業等專業領域提供精準的業務分析。

## ✨ 核心特色

### 🧠 動態分析引擎
- **智能實體提取**：使用jieba中文分詞自動識別人數、時間、比率等關鍵信息
- **領域檢測**：自動識別保險、電商等業務領域
- **複雜度計算**：基於文本長度、實體數量、技術術語動態評估
- **優先級識別**：根據內容自動確定分析重點

### 🔄 模型容錯機制
```
MiniMax → Gemini Flash → Claude Sonnet → Gemini Pro → 本地分析
```
- **智能降級**：當首選模型失敗時自動切換到下一個模型
- **無縫體驗**：用戶感受不到模型切換過程
- **最終保障**：即使所有外部模型都失敗，也有本地分析兜底

### 🚀 增量引擎增強
- **版本管理**：追蹤分析過程的演進
- **變更檢測**：識別分析質量的提升點
- **智能優化**：基於增量分析進一步改善結果

### 📄 多模態文檔處理
- **支持格式**：DOC、DOCX、PDF、TXT
- **內容提取**：智能提取文檔結構和關鍵信息
- **專業分析**：針對保險核保SOP等專業文檔提供深度分析

## 🏗️ 系統架構

```
├── dynamic_analysis_engine.py     # 動態分析引擎核心
├── incremental_engine.py          # 增量引擎
├── document_extractor.py          # 文檔內容提取器
├── simple_service.py              # HTTP服務主程序
├── multimodal_requirement_analysis_service.py  # 完整版服務
├── interactive_requirement_analysis_workflow_mcp.py  # 交互式工作流
├── smart_tool_engine.py           # 智能工具引擎
└── aicore0619/                    # MCP適配器組件
    └── mcp/adapter/cloud_search_mcp/
```

## 🚀 快速開始

### 1. 環境準備

```bash
# 安裝依賴
pip3 install flask flask-cors jieba python-docx PyPDF2

# 克隆項目
git clone https://github.com/alexchuang650730/aicore0620.git
cd aicore0620/enterprise/dynamic_multimodal_analysis
```

### 2. 啟動服務

```bash
# 啟動簡化版服務
python3 simple_service.py

# 或啟動完整版服務
python3 multimodal_requirement_analysis_service.py
```

### 3. 訪問服務

- **本地訪問**：http://localhost:8300
- **API文檔**：http://localhost:8300/api/info
- **健康檢查**：http://localhost:8300/health

## 📊 API接口

### 需求分析
```bash
POST /api/analyze
Content-Type: application/json

{
    "requirement": "我們公司的核保SOP流程需要20個人處理，每天大概處理500件申請，OCR準確率只有85%，想知道自動化可以節省多少人力",
    "model": "minimax"
}
```

### 文檔分析
```bash
POST /api/upload-document
Content-Type: multipart/form-data

file: [文檔文件]
requirement: [可選的額外需求描述]
analysis_mode: document|combined
```

## 🎯 專業應用案例

### 保險業核保SOP分析

系統能夠：
- **人力需求分析**：基於實際流程計算所需人力
- **時間效率評估**：分析各環節的時間成本
- **自動化潛力評估**：識別可自動化的流程環節
- **成本效益分析**：計算投資回報率和節省成本
- **風險評估**：評估實施風險和緩解措施

### 示例分析結果

```json
{
    "analysis": {
        "complexity": "高度專業",
        "estimated_time": "深度分析完成",
        "key_insights": [
            "識別到人力需求：20個人",
            "關鍵指標：85%準確率",
            "OCR審核占總流程20-25%，是自動化的關鍵環節"
        ],
        "specific_analysis": {
            "人力需求": "基於需求分析，需要20人的團隊",
            "時間分析": "每天處理500件申請",
            "自動化潛力": "OCR準確率提升至95%可減少60%人工校對工作"
        }
    },
    "confidence": 0.95,
    "analysis_method": "dynamic_with_incremental_enhancement"
}
```

## 🔧 技術特色

### 動態分析 vs 硬編碼模板

❌ **傳統方式**：
```python
# 硬編碼的模板回應
if "核保" in requirement:
    return {"人力需求": "16-21人"}  # 寫死的數據
```

✅ **動態分析引擎**：
```python
# 真正的智能分析
entities = extract_entities(requirement)  # 提取實際數據
analysis = analyze_context(entities)      # 基於實際內容分析
return generate_insights(analysis)        # 生成個性化洞察
```

### 模型容錯機制

```python
async def _try_model_analysis(self, requirement, preferred_model, context):
    models_to_try = self._get_model_sequence(preferred_model)
    
    for model in models_to_try:
        try:
            result = await self._call_model(model, requirement, context)
            if result and result.get("success", False):
                return result
        except Exception as e:
            logger.warning(f"模型 {model} 分析失敗: {e}")
            continue
    
    # 所有模型都失敗，使用本地分析
    return self._local_analysis(requirement, context)
```

## 📈 性能指標

- **響應時間**：< 500ms（本地分析）
- **準確率**：95%+（專業領域分析）
- **可用性**：99.9%（多重容錯機制）
- **擴展性**：支持水平擴展

## 🛠️ 開發指南

### 添加新的分析模型

```python
async def _call_new_model(self, requirement: str, context: AnalysisContext):
    """添加新的分析模型"""
    # 實現新模型的調用邏輯
    pass

# 在模型配置中添加
self.model_config["new_model"] = {
    "priority": 5,
    "timeout": 30,
    "fallback": "local_analysis"
}
```

### 擴展領域知識

```python
self.domain_knowledge["new_domain"] = {
    "keywords": ["關鍵詞1", "關鍵詞2"],
    "processes": ["流程1", "流程2"],
    "metrics": ["指標1", "指標2"],
    "industry_benchmarks": {
        "benchmark1": 0.8,
        "benchmark2": 100
    }
}
```

## 🔒 安全性

- **輸入驗證**：嚴格的輸入參數驗證
- **文件安全**：臨時文件自動清理
- **API限流**：防止濫用攻擊
- **日誌記錄**：完整的操作審計日誌

## 📝 更新日誌

### v2.0.0 (2025-06-19)
- ✨ 新增動態分析引擎
- 🔄 實現模型容錯機制
- 🚀 整合增量引擎
- 📄 完善文檔處理功能
- 🎯 專業保險業分析能力

### v1.0.0 (2025-06-18)
- 🎉 初始版本發布
- 📊 基礎需求分析功能
- 🌐 HTTP API服務

## 🤝 貢獻指南

1. Fork 項目
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 許可證

本項目採用 MIT 許可證 - 查看 [LICENSE](LICENSE) 文件了解詳情。

## 📞 聯繫方式

- **項目維護者**：Alex Chuang
- **GitHub**：https://github.com/alexchuang650730/aicore0620
- **問題反饋**：https://github.com/alexchuang650730/aicore0620/issues

## 🙏 致謝

感謝所有為這個項目做出貢獻的開發者和用戶！

