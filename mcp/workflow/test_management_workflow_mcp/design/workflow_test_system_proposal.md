# 🚀 七大工作流測試系統設計方案

## 📋 **方案概述**

基於現有的MCP測試架構，設計一個統一的工作流測試系統，支持下拉式選單選擇工作流，執行API測試和文生模板測試，提供curl命令模式和UI操作模式。

## 🎯 **七大工作流識別**

### **已確認的工作流**
1. **Coding Workflow MCP** - 編碼工作流
2. **Requirements Analysis MCP** - 需求分析工作流  
3. **Operations Workflow MCP** - 運營工作流
4. **Release Manager MCP** - 發布管理工作流
5. **Architecture Design MCP** - 架構設計工作流
6. **Developer Flow MCP** - 開發者工作流
7. **Test Management Workflow MCP** - 測試管理工作流

## 🏗️ **現有測試結構分析**

### **標準測試目錄結構**
```
mcp/workflow/{workflow_name}/
├── testcases/
│   ├── main_testcase_template.md
│   ├── {workflow}_function_testcase_template.md
│   ├── testcase_config.yaml
│   └── stress_test_case.md (部分有)
├── unit_tests/
│   ├── test_{workflow}.py
│   └── test_{workflow}_comprehensive.py
└── integration_tests/
    └── test_{workflow}_integration.py
```

### **測試類型分類**
- **Unit Tests**: 單元測試 (API測試)
- **Integration Tests**: 集成測試 (文生模板)
- **Testcases**: 測試用例模板
- **Performance Tests**: 性能測試

## 🎨 **界面設計方案**

### **主界面布局**
```
┌─────────────────────────────────────────────────────────┐
│ 🚀 AICore0620 工作流測試系統                              │
├─────────────────────────────────────────────────────────┤
│ 📋 工作流選擇                                            │
│ [下拉選單: 選擇工作流] ▼                                  │
│                                                         │
│ 🔧 測試類型                                              │
│ ○ API測試 (單元測試)    ○ 文生模板 (集成測試)             │
│                                                         │
│ 🎯 操作模式                                              │
│ ○ UI操作模式           ○ curl命令模式                    │
│                                                         │
│ ⚙️ 測試參數                                              │
│ [參數輸入區域]                                           │
│                                                         │
│ [執行測試] [生成curl命令] [清除結果]                      │
│                                                         │
│ 📊 測試結果                                              │
│ [結果顯示區域]                                           │
└─────────────────────────────────────────────────────────┘
```

## 🔧 **功能設計方案**

### **1. 工作流選擇器**
```javascript
const workflows = [
    { id: 'coding_workflow_mcp', name: '編碼工作流', port: 8888 },
    { id: 'requirements_analysis_mcp', name: '需求分析工作流', port: 8100 },
    { id: 'operations_workflow_mcp', name: '運營工作流', port: 8091 },
    { id: 'release_manager_mcp', name: '發布管理工作流', port: 8092 },
    { id: 'architecture_design_mcp', name: '架構設計工作流', port: 8093 },
    { id: 'developer_flow_mcp', name: '開發者工作流', port: 8094 },
    { id: 'test_management_workflow_mcp', name: '測試管理工作流', port: 8321 }
];
```

### **2. 測試類型定義**
```javascript
const testTypes = {
    api_test: {
        name: 'API測試 (單元測試)',
        description: '測試工作流的API端點和核心功能',
        endpoint: '/api/unit-test',
        method: 'POST'
    },
    template_test: {
        name: '文生模板 (集成測試)', 
        description: '測試完整的工作流程和模板生成',
        endpoint: '/api/integration-test',
        method: 'POST'
    }
};
```

### **3. 操作模式設計**
```javascript
const operationModes = {
    ui_mode: {
        name: 'UI操作模式',
        description: '通過圖形界面執行測試',
        features: ['參數表單', '結果可視化', '錯誤提示']
    },
    curl_mode: {
        name: 'curl命令模式',
        description: '生成curl命令供命令行執行',
        features: ['命令生成', '參數轉換', '腳本導出']
    }
};
```

## 🚀 **API設計方案**

### **後端API端點**
```python
# 工作流測試API
@app.route('/api/workflow-test', methods=['POST'])
def workflow_test():
    """統一的工作流測試端點"""
    
@app.route('/api/generate-curl', methods=['POST']) 
def generate_curl():
    """生成curl命令"""
    
@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    """獲取所有可用工作流"""
    
@app.route('/api/testcases/<workflow_id>', methods=['GET'])
def get_testcases(workflow_id):
    """獲取指定工作流的測試用例"""
```

### **測試執行流程**
```python
def execute_workflow_test(workflow_id, test_type, params):
    """
    執行工作流測試
    
    Args:
        workflow_id: 工作流ID
        test_type: 測試類型 (api_test/template_test)
        params: 測試參數
    
    Returns:
        測試結果和詳細信息
    """
```

## 📊 **測試結果展示**

### **結果數據結構**
```json
{
    "success": true,
    "workflow_id": "coding_workflow_mcp",
    "test_type": "api_test",
    "execution_time": 1.23,
    "results": {
        "status": "passed",
        "test_count": 5,
        "passed": 4,
        "failed": 1,
        "details": [...]
    },
    "curl_command": "curl -X POST ...",
    "timestamp": "2025-06-21T05:00:00Z"
}
```

### **UI展示組件**
- **狀態指示器**: 成功/失敗/進行中
- **進度條**: 測試執行進度
- **結果表格**: 詳細測試結果
- **錯誤日誌**: 失敗原因分析
- **性能指標**: 執行時間、資源使用

## 🔄 **實施計劃**

### **Phase 1: 前端重構**
- 重新設計HTML界面
- 實現下拉選單和表單
- 添加結果展示組件

### **Phase 2: 後端API開發**
- 實現統一測試API
- 集成現有測試用例
- 添加curl命令生成

### **Phase 3: 測試集成**
- 連接各工作流測試
- 實現測試用例加載
- 添加錯誤處理

### **Phase 4: 部署驗證**
- 本地測試驗證
- EC2部署更新
- 功能完整性測試

## 🎯 **預期效果**

1. **統一測試入口**: 一個界面測試所有工作流
2. **靈活測試方式**: 支持UI和命令行兩種模式
3. **完整測試覆蓋**: API測試和集成測試全覆蓋
4. **易於使用**: 直觀的界面和清晰的結果展示
5. **開發友好**: 自動生成curl命令，便於自動化

這個方案充分利用了現有的測試架構，提供了一個統一、靈活、易用的工作流測試系統。

