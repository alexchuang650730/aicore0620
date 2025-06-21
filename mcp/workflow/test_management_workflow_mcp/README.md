# Test Management Workflow MCP - 七大工作流測試系統

## 📋 **項目概述**

本項目為AICore0620架構中的測試管理工作流，提供統一的七大工作流測試系統，支持API測試（單元測試）和文生模板（集成測試），包含curl命令模式和UI操作模式。

## 🏗️ **目錄結構**

```
mcp/workflow/test_management_workflow_mcp/
├── README.md                                    # 本文檔
├── __init__.py                                  # 模組初始化
├── pure_ai_test_management_workflow_mcp.py      # 核心工作流邏輯
├── test_manager.py                              # 測試管理器
├── workflow_engine.py                           # 工作流引擎
├── config/                                      # 配置文件
├── design/                                      # 設計文檔
│   ├── workflow_test_system_proposal.md         # 完整方案設計
│   ├── test_architecture_relationship.md        # 與現有測試架構關係
│   └── workflow_test_system_design.md          # 系統設計分析
├── docs/                                        # 文檔目錄
├── testcases/                                   # 測試用例模板
├── unit_tests/                                  # 單元測試
├── integration_tests/                           # 集成測試
└── ui_system/                                   # UI系統
    ├── backend/                                 # 後端服務
    ├── frontend/                                # 前端界面
    ├── config/                                  # UI配置
    └── docs/                                    # UI文檔
```

## 🎯 **核心功能**

### **1. 七大工作流支持**
- Coding Workflow MCP - 編碼工作流
- Requirements Analysis MCP - 需求分析工作流
- Operations Workflow MCP - 運營工作流
- Release Manager MCP - 發布管理工作流
- Architecture Design MCP - 架構設計工作流
- Developer Flow MCP - 開發者工作流
- Test Management Workflow MCP - 測試管理工作流

### **2. 測試類型**
- **API測試（單元測試）**: 執行各工作流的unit_tests/
- **文生模板（集成測試）**: 執行各工作流的integration_tests/

### **3. 操作模式**
- **UI操作模式**: 圖形界面操作，直觀易用
- **curl命令模式**: 命令行操作，便於自動化

## 🔧 **技術架構**

### **與現有測試架構的關係**
本系統**不替代**現有測試架構，而是作為**統一的測試執行器**：

```
統一測試界面 (本系統)
    ↓ 調用
現有測試架構 (各工作流的unit_tests/integration_tests/)
```

### **實現方式**
- **前端**: 響應式HTML + JavaScript
- **後端**: Flask API統一測試端點
- **測試集成**: 直接調用現有pytest測試
- **命令生成**: 動態curl命令構建

## 🚀 **使用方法**

### **本地部署**
```bash
cd mcp/workflow/test_management_workflow_mcp/ui_system
pip install -r backend/requirements.txt
python backend/ui_backend_server.py
```

### **訪問界面**
- 本地: http://localhost:5001
- EC2: http://18.212.97.173:5001

### **API使用**
```bash
# 執行單元測試
curl -X POST http://localhost:5001/api/workflow-test \
  -H "Content-Type: application/json" \
  -d '{"workflow_id": "coding_workflow_mcp", "test_type": "unit"}'

# 執行集成測試
curl -X POST http://localhost:5001/api/workflow-test \
  -H "Content-Type: application/json" \
  -d '{"workflow_id": "coding_workflow_mcp", "test_type": "integration"}'
```

## 📊 **設計文檔**

詳細的設計文檔位於 `design/` 目錄：

1. **workflow_test_system_proposal.md** - 完整的系統設計方案
2. **test_architecture_relationship.md** - 與現有測試架構的關係說明
3. **workflow_test_system_design.md** - 七大工作流和測試需求分析

## 🎯 **項目狀態**

- ✅ **需求分析**: 完成七大工作流識別和測試架構分析
- ✅ **方案設計**: 完成統一測試系統設計方案
- ✅ **UI原型**: 完成基礎UI界面和後端API
- 🔄 **功能實現**: 正在實施七大工作流集成
- ⏳ **測試驗證**: 待完成功能測試和部署驗證

## 📞 **聯繫信息**

如有問題或建議，請參考design/目錄中的詳細設計文檔，或聯繫開發團隊。

---

**本項目是AICore0620架構重構的重要組成部分，旨在提供統一、高效、易用的工作流測試解決方案。**

