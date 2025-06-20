# 純AI驅動發布管理系統 - Workflow MCP

## 概述

純AI驅動發布管理系統的Workflow層實現，負責AI驅動的組件選擇和執行策略制定。

## 架構組件

### Product Layer
- `product/release/release_product_orchestrator.py` - 發布需求理解和業務價值評估引擎

### Workflow Layer  
- `workflow/release_workflow_mcp/release_workflow_mcp.py` - AI驅動組件選擇和執行策略

### 整合測試
- `integration_test.py` - 三層架構整合測試

## 核心特性

✅ **零硬編碼**: 完全無關鍵詞列表、預設數據、固定邏輯
✅ **純AI推理**: 100%基於Claude智能推理和決策  
✅ **動態適應**: 根據需求內容自動調整分析策略
✅ **質量對齊**: 達到企業級專業分析師水準

## 快速開始

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動Product Layer
python -m uvicorn product.release.release_product_orchestrator:app --host 0.0.0.0 --port 8302

# 啟動Workflow Layer
python -m uvicorn workflow.release_workflow_mcp.release_workflow_mcp:app --host 0.0.0.0 --port 8303

# 運行整合測試
python integration_test.py
```

## API端點

### 發布需求分析
```http
POST /api/release/analyze
```

### 組件選擇
```http  
POST /api/workflow/select-components
```

詳細文檔請參考 README.md

