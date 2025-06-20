# AICore0620 目錄規範 3.0

## 🎯 **設計原則**

1. **分層架構** - 明確的Product、Workflow、Adapter三層分離
2. **功能導向** - 按功能模組組織，避免重複結構
3. **純AI驅動** - 以pure_ai_driven_system為核心，廢棄模板化組件
4. **統一管理** - 集中配置、文檔、服務管理

## 📁 **目錄規範 3.0 結構**

```
aicore0620/                           # 項目根目錄
├── README.md                         # 項目總覽
├── requirements.txt                  # 統一依賴管理
├── sandbox_server.py                 # 主AI分析服務器
├── config/                          # 全局配置
│   ├── global_config.py
│   └── environment_config.py
├── docs/                            # 全局文檔
│   ├── README.md                    # 文檔索引
│   ├── api_documentation/           # API文檔
│   ├── architecture/                # 架構文檔
│   └── pure_ai_driven/             # 純AI驅動系統文檔
├── product/                         # Product Layer - 產品層
│   ├── __init__.py
│   ├── enterprise/                  # 企業級產品 (NEW)
│   │   ├── __init__.py
│   │   ├── enterprise_orchestrator.py  # 純AI驅動企業編排器
│   │   └── README.md
│   └── personal/                    # 個人級產品
│       └── product_orchestrator/
├── workflow/                        # Workflow Layer - 工作流層 (NEW)
│   ├── __init__.py
│   ├── orchestrator/                # 工作流編排器
│   │   ├── __init__.py
│   │   └── workflow_orchestrator.py
│   └── requirements_analysis_mcp/   # 需求分析工作流 (純AI版本)
│       ├── __init__.py
│       ├── requirements_analysis_mcp.py
│       ├── integration_tests/
│       └── testcases/
├── adapter/                         # Adapter Layer - 適配器層 (NEW)
│   ├── __init__.py
│   └── advanced_analysis_mcp/       # 高級分析適配器
│       ├── __init__.py
│       ├── src/
│       │   ├── __init__.py
│       │   └── advanced_ai_engine.py
│       └── tests/
├── adminboard/                      # 管理界面
│   └── requrement_analysis/         # 需求分析UI
├── mcp/                            # 舊版MCP組件 (逐步廢棄)
│   ├── adapter/                    # 將被adapter/取代
│   ├── workflow/                   # 將被workflow/取代
│   └── coordinator/                # 保留協調器功能
├── opensource/                      # 開源組件
│   ├── cli_tool/
│   └── ocr/
├── personal/                        # 個人級功能 (舊版)
│   └── product_orchestrator/
├── enterprise/                      # 企業級功能 (舊版，將廢棄)
└── scripts/                         # 工具腳本
    ├── deployment/
    └── testing/
```

## 🔄 **從規範2.0到3.0的主要變更**

### 新增頂層目錄
1. **product/** - 統一的產品層目錄
2. **workflow/** - 統一的工作流層目錄  
3. **adapter/** - 統一的適配器層目錄

### 目錄遷移計劃
```bash
# Product Layer
pure_ai_driven_system/product/enterprise/ → product/enterprise/

# Workflow Layer  
pure_ai_driven_system/workflow/ → workflow/

# Adapter Layer
pure_ai_driven_system/adapter/ → adapter/

# 主服務器
pure_ai_driven_system/sandbox_server.py → sandbox_server.py

# 文檔
pure_ai_driven_system/docs/ → docs/pure_ai_driven/
```

### 廢棄組件
```bash
# 廢棄舊版模板化組件
mcp/workflow/requirements_analysis_mcp/ → 廢棄 (保留純AI版本)
mcp/adapter/advanced_analysis_mcp/ → 廢棄 (保留純AI版本)
enterprise/ → 廢棄 (功能移至product/enterprise/)
```

## 🎯 **三層架構映射**

### Product Layer (產品層)
```
product/
├── enterprise/                      # 企業級產品
│   └── enterprise_orchestrator.py  # 純AI驅動企業編排器
└── personal/                        # 個人級產品
    └── product_orchestrator/
```

### Workflow Layer (工作流層)
```
workflow/
├── orchestrator/                    # 工作流編排器
│   └── workflow_orchestrator.py
└── requirements_analysis_mcp/       # 純AI需求分析工作流
    └── requirements_analysis_mcp.py
```

### Adapter Layer (適配器層)
```
adapter/
└── advanced_analysis_mcp/           # 高級分析適配器
    └── src/
        └── advanced_ai_engine.py   # 終極Claude分析引擎
```

## 📋 **重構執行原則**

### 1. 以Pure AI為主
- **保留**: pure_ai_driven_system中的所有組件
- **廢棄**: 原有的模板化、硬編碼組件
- **原則**: 100%純AI驅動，零硬編碼

### 2. 功能完整性
- **三層架構**: Product → Workflow → Adapter 調用鏈完整
- **API服務**: sandbox_server.py 提供完整API服務
- **UI界面**: adminboard 提供用戶界面

### 3. 向後兼容
- **漸進遷移**: 保留mcp/目錄，逐步廢棄
- **功能對等**: 新架構提供相同或更好的功能
- **平滑過渡**: 確保服務不中斷

## 🚀 **實施優勢**

### 架構優勢
1. **清晰分層** - 三層架構更加明確
2. **統一管理** - 同類組件集中管理
3. **易於擴展** - 新功能按層級添加
4. **減少冗餘** - 消除重複目錄結構

### 技術優勢
1. **純AI驅動** - 100%基於AI推理，無硬編碼
2. **高性能** - 95%信心度，專業級分析
3. **可維護性** - 代碼組織清晰，易於維護
4. **可測試性** - 分層測試，功能驗證完整

### 業務優勢
1. **企業就緒** - 企業級功能完整
2. **擴展性強** - 支持多種產品類型
3. **用戶友好** - 完整的UI和API接口
4. **部署簡單** - 統一的部署和配置

## 📊 **遷移對照表**

| 舊路徑 | 新路徑 | 狀態 |
|--------|--------|------|
| `pure_ai_driven_system/product/enterprise/` | `product/enterprise/` | 遷移 |
| `pure_ai_driven_system/workflow/` | `workflow/` | 遷移 |
| `pure_ai_driven_system/adapter/` | `adapter/` | 遷移 |
| `pure_ai_driven_system/sandbox_server.py` | `sandbox_server.py` | 遷移 |
| `pure_ai_driven_system/docs/` | `docs/pure_ai_driven/` | 遷移 |
| `mcp/workflow/requirements_analysis_mcp/` | - | 廢棄 |
| `mcp/adapter/advanced_analysis_mcp/` | - | 廢棄 |
| `enterprise/` | - | 廢棄 |

---

**AICore0620 目錄規範 3.0 - 純AI驅動，企業就緒，架構清晰** 🎯

