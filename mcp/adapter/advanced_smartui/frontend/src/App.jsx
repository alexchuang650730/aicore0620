import React, { useState, useEffect } from 'react';
import './App.css';

// 圖標組件
import { 
  Code, 
  Edit, 
  Rocket, 
  MessageCircle, 
  Activity, 
  GitBranch, 
  Zap,
  CheckCircle,
  Clock,
  Users,
  Server,
  Send
} from 'lucide-react';

// SmartUI 智慧感知功能
const useSmartUILayout = () => {
  const [layoutOptimized, setLayoutOptimized] = useState(false);
  const [smartUIActive, setSmartUIActive] = useState(false);
  const [inputOptimized, setInputOptimized] = useState(false);
  const [dialogAligned, setDialogAligned] = useState(false);
  const [deploymentCardAdded, setDeploymentCardAdded] = useState(false);
  const [voiceControlActive, setVoiceControlActive] = useState(false);

  // 智慧感知指令解析器
  const parseSmartCommand = (command) => {
    const lowerCommand = command.toLowerCase();
    
    // 節點操控指令
    if (lowerCommand.includes('編碼') || lowerCommand.includes('coding')) {
      return { type: 'node_action', target: 'coding', action: 'activate' };
    }
    if (lowerCommand.includes('測試') || lowerCommand.includes('testing')) {
      return { type: 'node_action', target: 'testing', action: 'activate' };
    }
    if (lowerCommand.includes('部署') || lowerCommand.includes('deployment')) {
      return { type: 'node_action', target: 'deployment', action: 'activate' };
    }
    
    // 佈局控制指令
    if (lowerCommand.includes('橫向') || lowerCommand.includes('水平')) {
      return { type: 'layout_action', target: 'horizontal', action: 'apply' };
    }
    if (lowerCommand.includes('垂直') || lowerCommand.includes('縱向')) {
      return { type: 'layout_action', target: 'vertical', action: 'apply' };
    }
    
    // 介面優化指令
    if (lowerCommand.includes('優化輸入') || lowerCommand.includes('放大輸入')) {
      return { type: 'ui_action', target: 'input', action: 'optimize' };
    }
    if (lowerCommand.includes('對齊') || lowerCommand.includes('調整位置')) {
      return { type: 'ui_action', target: 'dialog', action: 'align' };
    }
    
    // 狀態查詢指令
    if (lowerCommand.includes('狀態') || lowerCommand.includes('進度')) {
      return { type: 'query_action', target: 'status', action: 'show' };
    }
    
    return null;
  };

  // 執行智慧感知指令
  const executeSmartCommand = (command, callbacks) => {
    const parsedCommand = parseSmartCommand(command);
    
    if (!parsedCommand) return false;
    
    setSmartUIActive(true);
    
    setTimeout(() => {
      switch (parsedCommand.type) {
        case 'node_action':
          if (callbacks.onNodeClick) {
            callbacks.onNodeClick(parsedCommand.target);
          }
          break;
          
        case 'layout_action':
          if (parsedCommand.target === 'horizontal') {
            setLayoutOptimized(true);
          } else {
            setLayoutOptimized(false);
          }
          break;
          
        case 'ui_action':
          if (parsedCommand.target === 'input') {
            setInputOptimized(true);
          } else if (parsedCommand.target === 'dialog') {
            setDialogAligned(true);
          }
          break;
          
        case 'query_action':
          if (callbacks.onStatusQuery) {
            callbacks.onStatusQuery();
          }
          break;
      }
      
      setSmartUIActive(false);
    }, 1000);
    
    return true;
  };

  // 語音控制
  const startVoiceControl = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      
      recognition.lang = 'zh-TW';
      recognition.continuous = false;
      recognition.interimResults = false;
      
      recognition.onstart = () => {
        setVoiceControlActive(true);
        console.log('🎤 SmartUI: 語音控制已啟動');
      };
      
      recognition.onresult = (event) => {
        const command = event.results[0][0].transcript;
        console.log('🎤 SmartUI: 接收到語音指令:', command);
        
        // 這裡需要回調函數來執行指令
        if (window.smartUICallbacks) {
          executeSmartCommand(command, window.smartUICallbacks);
        }
      };
      
      recognition.onerror = (event) => {
        console.error('🎤 SmartUI: 語音識別錯誤:', event.error);
        setVoiceControlActive(false);
      };
      
      recognition.onend = () => {
        setVoiceControlActive(false);
        console.log('🎤 SmartUI: 語音控制已結束');
      };
      
      recognition.start();
    } else {
      console.warn('🎤 SmartUI: 瀏覽器不支援語音識別');
    }
  };

  // 智慧感知佈局優化
  const optimizeLayout = () => {
    setSmartUIActive(true);
    
    // 模擬智慧感知分析過程
    setTimeout(() => {
      setLayoutOptimized(true);
      console.log('🤖 SmartUI: 檢測到用戶需要橫向三節點佈局');
      console.log('🎯 SmartUI: 自動調整為最佳橫向排列');
    }, 1000);
  };

  // 智慧感知輸入框優化
  const optimizeInput = () => {
    setSmartUIActive(true);
    
    setTimeout(() => {
      setInputOptimized(true);
      console.log('🤖 SmartUI: 檢測到用戶需要移除輸入框旁按鈕');
      console.log('🎯 SmartUI: 自動放大輸入框並移除干擾按鈕');
    }, 1500);
  };

  // 智慧感知對話區域對齊
  const alignDialog = () => {
    setSmartUIActive(true);
    
    setTimeout(() => {
      setDialogAligned(true);
      console.log('🤖 SmartUI: 檢測到用戶需要調整對話區域位置');
      console.log('🎯 SmartUI: 自動對齊對話區域與左側卡片');
    }, 2000);
  };

  // 智慧感知添加部署狀態卡片
  const addDeploymentCard = () => {
    setSmartUIActive(true);
    
    setTimeout(() => {
      setDeploymentCardAdded(true);
      console.log('🤖 SmartUI: 檢測到用戶需要部署狀態監控');
      console.log('🎯 SmartUI: 自動添加部署狀態卡片');
    }, 2500);
  };

  return { 
    layoutOptimized, 
    smartUIActive, 
    optimizeLayout, 
    inputOptimized, 
    optimizeInput, 
    dialogAligned, 
    alignDialog,
    deploymentCardAdded,
    addDeploymentCard,
    voiceControlActive,
    startVoiceControl,
    executeSmartCommand,
    parseSmartCommand
  };
};

function App() {
  const [progress, setProgress] = useState(75);
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'user',
      content: '很好！我需要實時看到所有工作流的狀態，特別是編碼、測試、部署三個節點的進度。',
      timestamp: new Date()
    },
    {
      id: 2,
      type: 'ai',
      content: '✅ 完全理解！右側面板已經集成了三節點工作流Dashboard，實時顯示三大核心功能模組的運行狀態和性能指標。',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  
  // 三節點狀態管理
  const [nodeStates, setNodeStates] = useState({
    coding: { progress: 100, quality: 100, compliance: 92, status: 'completed', lastUpdate: new Date() },
    testing: { progress: 85, coverage: 85, testCases: 3, status: 'running', lastUpdate: new Date() },
    deployment: { progress: 85, successCount: 12, avgTime: '2.3s', status: 'deploying', lastUpdate: new Date() }
  });
  
  // 部署狀態
  const [deploymentProgress, setDeploymentProgress] = useState(85);
  const [serviceStates, setServiceStates] = useState({
    frontend: 'running',
    backend: 'running',
    database: 'connecting'
  });
  
  // 使用 SmartUI 智慧感知功能
  const { 
    layoutOptimized, 
    smartUIActive, 
    optimizeLayout, 
    inputOptimized, 
    optimizeInput, 
    dialogAligned, 
    alignDialog,
    deploymentCardAdded,
    addDeploymentCard,
    voiceControlActive,
    startVoiceControl,
    executeSmartCommand,
    parseSmartCommand
  } = useSmartUILayout();

  // 設置 SmartUI 回調函數
  useEffect(() => {
    window.smartUICallbacks = {
      onNodeClick: handleNodeClick,
      onStatusQuery: () => {
        const statusMessage = {
          id: messages.length + Date.now(),
          type: 'ai',
          content: `📊 系統狀態報告：
編碼節點：${nodeStates.coding.status} (${nodeStates.coding.progress}%)
測試節點：${nodeStates.testing.status} (${nodeStates.testing.progress}%)
部署節點：${nodeStates.deployment.status} (${nodeStates.deployment.progress}%)
總體進度：${Math.round(progress)}%`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, statusMessage]);
      }
    };
    
    return () => {
      delete window.smartUICallbacks;
    };
  }, [messages, nodeStates, progress]);

  // 自動觸發智慧感知優化
  useEffect(() => {
    const timer = setTimeout(() => {
      optimizeLayout();
    }, 2000);
    
    // 自動觸發輸入框優化
    const inputTimer = setTimeout(() => {
      optimizeInput();
    }, 4000);
    
    // 自動觸發對話區域對齊
    const dialogTimer = setTimeout(() => {
      alignDialog();
    }, 6000);

    // 自動觸發部署狀態卡片添加
    const deploymentTimer = setTimeout(() => {
      addDeploymentCard();
    }, 8000);
    
    return () => {
      clearTimeout(timer);
      clearTimeout(inputTimer);
      clearTimeout(dialogTimer);
      clearTimeout(deploymentTimer);
    };
  }, []);

  // 模擬進度更新
  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + Math.random() * 2 - 1;
        return Math.max(0, Math.min(100, newProgress));
      });
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  // 節點點擊處理函數
  const handleNodeClick = (nodeType) => {
    const timestamp = new Date();
    
    setNodeStates(prev => {
      const newStates = { ...prev };
      
      switch (nodeType) {
        case 'coding':
          newStates.coding = {
            ...prev.coding,
            progress: Math.min(100, prev.coding.progress + Math.floor(Math.random() * 10)),
            quality: Math.min(100, prev.coding.quality + Math.floor(Math.random() * 5)),
            compliance: Math.max(85, Math.min(100, prev.coding.compliance + Math.floor(Math.random() * 8) - 3)),
            status: prev.coding.progress >= 95 ? 'completed' : 'running',
            lastUpdate: timestamp
          };
          break;
          
        case 'testing':
          newStates.testing = {
            ...prev.testing,
            progress: Math.min(100, prev.testing.progress + Math.floor(Math.random() * 15)),
            coverage: Math.min(100, prev.testing.coverage + Math.floor(Math.random() * 10)),
            testCases: prev.testing.testCases + Math.floor(Math.random() * 3),
            status: prev.testing.progress >= 95 ? 'completed' : 'running',
            lastUpdate: timestamp
          };
          break;
          
        case 'deployment':
          const newProgress = Math.min(100, prev.deployment.progress + Math.floor(Math.random() * 20));
          newStates.deployment = {
            ...prev.deployment,
            progress: newProgress,
            successCount: prev.deployment.successCount + (newProgress >= 100 ? 1 : 0),
            avgTime: (Math.random() * 2 + 1.5).toFixed(1) + 's',
            status: newProgress >= 100 ? 'completed' : 'deploying',
            lastUpdate: timestamp
          };
          
          // 更新部署進度
          setDeploymentProgress(newProgress);
          
          // 更新服務狀態
          if (newProgress >= 100) {
            setServiceStates({
              frontend: 'running',
              backend: 'running',
              database: 'running'
            });
          }
          break;
      }
      
      return newStates;
    });
    
    // 添加 AI 回應消息
    const responses = {
      coding: [
        '🔧 編碼節點已激活！正在執行代碼質量檢查和架構合規驗證...',
        '💻 代碼編譯完成，質量分析中...',
        '✨ 智能代碼優化建議已生成！'
      ],
      testing: [
        '🧪 測試節點啟動！正在執行自動化測試套件...',
        '📊 測試覆蓋率分析中，新增測試用例...',
        '✅ 單元測試和集成測試進行中...'
      ],
      deployment: [
        '🚀 部署節點激活！正在準備生產環境部署...',
        '📦 容器化打包完成，開始部署流程...',
        '🌐 服務正在上線，監控系統已就緒...'
      ]
    };
    
    const responseMessage = {
      id: messages.length + Date.now(),
      type: 'ai',
      content: responses[nodeType][Math.floor(Math.random() * responses[nodeType].length)],
      timestamp: timestamp
    };
    
    setMessages(prev => [...prev, responseMessage]);
    
    // 更新總進度
    setProgress(prev => Math.min(100, prev + Math.floor(Math.random() * 8) + 2));
    
    console.log(`🤖 SmartUI: ${nodeType} 節點被激活，狀態已更新`);
  };

  const handleSendMessage = () => {
    if (inputMessage.trim()) {
      // 檢查是否為 SmartUI 智慧感知指令
      const isSmartCommand = executeSmartCommand(inputMessage, {
        onNodeClick: handleNodeClick,
        onStatusQuery: () => {
          const statusMessage = {
            id: messages.length + Date.now(),
            type: 'ai',
            content: `📊 系統狀態報告：
編碼節點：${nodeStates.coding.status} (${nodeStates.coding.progress}%)
測試節點：${nodeStates.testing.status} (${nodeStates.testing.progress}%)
部署節點：${nodeStates.deployment.status} (${nodeStates.deployment.progress}%)
總體進度：${Math.round(progress)}%`,
            timestamp: new Date()
          };
          setMessages(prev => [...prev, statusMessage]);
        }
      });
      
      const newMessage = {
        id: messages.length + 1,
        type: 'user',
        content: inputMessage,
        timestamp: new Date()
      };
      setMessages([...messages, newMessage]);
      setInputMessage('');
      
      // 如果是智慧感知指令，顯示確認消息
      if (isSmartCommand) {
        setTimeout(() => {
          const aiResponse = {
            id: messages.length + 2,
            type: 'ai',
            content: '✅ SmartUI 智慧感知指令已執行！',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, aiResponse]);
        }, 500);
      } else {
        // 一般對話回覆
        setTimeout(() => {
          const aiResponse = {
            id: messages.length + 2,
            type: 'ai',
            content: '我正在處理您的請求，請稍候...',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, aiResponse]);
        }, 1000);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* 頂部導航 */}
      <header className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white p-4">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
              <Zap className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold">PowerAutomation AI</h1>
              <p className="text-sm opacity-90">智慧UI助手 - 在線 | MCP協調中</p>
            </div>
          </div>
          <div className="flex space-x-2">
            {/* SmartUI 語音控制按鈕 */}
            <button 
              onClick={startVoiceControl}
              className={`px-4 py-2 rounded-lg transition-all duration-300 ${
                voiceControlActive 
                  ? 'bg-red-500 text-white animate-pulse' 
                  : 'bg-white/20 hover:bg-white/30 text-white'
              }`}
            >
              🎤 {voiceControlActive ? '聆聽中...' : '語音控制'}
            </button>
            <button className="px-4 py-2 bg-white/20 rounded-lg hover:bg-white/30 transition-colors">
              Manus
            </button>
            <button className="px-4 py-2 bg-white/20 rounded-lg hover:bg-white/30 transition-colors">
              應用
            </button>
            <button className="px-4 py-2 bg-white/20 rounded-lg hover:bg-white/30 transition-colors">
              飛書
            </button>
          </div>
          <div className="flex items-center space-x-3">
            <h2 className="text-lg font-semibold">三節點工作流Dashboard</h2>
            {smartUIActive && (
              <div className="flex items-center space-x-2">
                <Zap className="w-4 h-4 animate-pulse" />
                <span className="text-sm">SmartUI 運行中</span>
              </div>
            )}
          </div>
        </div>
      </header>

      <div className="container mx-auto p-6">
        <div className="grid grid-cols-12 gap-6">
          {/* 左側狀態卡片 */}
          <div className="col-span-3 space-y-4">
            {/* 系統狀態監控 */}
            <div className="bg-white rounded-xl p-4 shadow-lg border border-gray-100">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="font-semibold text-gray-800">系統狀態監控</span>
                </div>
              </div>
            </div>

            {/* MCP協調器 */}
            <div className="bg-gradient-to-br from-blue-100 to-blue-200 rounded-xl p-4 shadow-lg">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="font-semibold text-blue-800">MCP協調器</span>
                </div>
                <span className="text-sm bg-blue-600 text-white px-2 py-1 rounded">運行中</span>
              </div>
              <p className="text-sm text-blue-700 mb-3">統一工作流協調 | 智能介入管理</p>
              <ul className="text-xs text-blue-600 space-y-1">
                <li>• Owen BB本地模型: 活躍</li>
                <li>• RL-SRT學習引擎: 運行</li>
                <li>• 開發介入檢測: 啟用</li>
                <li>• 架構合規檢查: 實時</li>
              </ul>
            </div>

            {/* 飛書集成 */}
            <div className="bg-gradient-to-br from-green-100 to-green-200 rounded-xl p-4 shadow-lg">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="font-semibold text-green-800">飛書集成</span>
                </div>
                <span className="text-sm bg-green-600 text-white px-2 py-1 rounded">已連接</span>
              </div>
              <p className="text-sm text-green-700 mb-3">實時通知 | 團隊協作 | 移動端同步</p>
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-green-800">24</div>
                  <div className="text-xs text-green-600">今日通知</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-green-800">3</div>
                  <div className="text-xs text-green-600">活躍群組</div>
                </div>
              </div>
            </div>

            {/* GitHub同步 */}
            <div className="bg-gradient-to-br from-yellow-100 to-yellow-200 rounded-xl p-4 shadow-lg">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="font-semibold text-yellow-800">GitHub同步</span>
                </div>
                <span className="text-sm bg-yellow-600 text-white px-2 py-1 rounded">同步中</span>
              </div>
              <p className="text-sm text-yellow-700 mb-2">powerauto_ai_0.53 | v0.6分支</p>
              <ul className="text-xs text-yellow-600 space-y-1 mb-3">
                <li>• Webhook: 正常監聽</li>
                <li>• 自動部署: 啟用</li>
                <li>• 代碼質量檢查: 通過</li>
              </ul>
              <div className="text-xs text-yellow-600">最後同步: 2分鐘前</div>
            </div>
          </div>

          {/* SmartUI 智慧感知中間主要區域 */}
          <div className={`col-span-6 transition-all duration-1000 ${
            dialogAligned ? 'space-y-4 mt-8' : 'space-y-6'
          }`}>
            {/* 進度條區域 - SmartUI 智慧感知調整 */}
            <div className={`bg-white rounded-xl p-6 shadow-lg transition-all duration-1000 ${
              dialogAligned ? 'transform translate-y-4' : ''
            }`}>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <Code className="w-6 h-6 text-blue-600" />
                  <span className="text-lg font-semibold">正在創建智慧UI Dashboard...</span>
                </div>
                <span className="text-lg font-bold text-blue-600">{Math.round(progress)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 mb-6">
                <div 
                  className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-500"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>

              {/* 快捷操作按鈕 */}
              <div className="grid grid-cols-2 gap-4">
                <button className="flex items-center justify-between p-4 bg-blue-50 hover:bg-blue-100 rounded-lg border border-blue-200 transition-colors">
                  <span className="text-blue-700">查看GitHub最新狀態</span>
                  <span className="text-sm bg-blue-500 text-white px-3 py-1 rounded">立即查看</span>
                </button>
                <button className="flex items-center justify-between p-4 bg-cyan-50 hover:bg-cyan-100 rounded-lg border border-cyan-200 transition-colors">
                  <span className="text-cyan-700">測試飛書通知功能</span>
                  <span className="text-sm bg-cyan-500 text-white px-3 py-1 rounded">發送測試</span>
                </button>
                <button className="flex items-center justify-between p-4 bg-green-50 hover:bg-green-100 rounded-lg border border-green-200 transition-colors">
                  <span className="text-green-700">檢查MCP協調器狀態</span>
                  <span className="text-sm bg-green-500 text-white px-3 py-1 rounded">系統檢查</span>
                </button>
              </div>
            </div>

            {/* SmartUI 智慧感知 AI 對話區域與部署狀態 */}
            <div className={`grid grid-cols-2 gap-6 transition-all duration-1000 ${
              dialogAligned ? 'transform translate-y-8 mt-6' : ''
            }`}>
              
              {/* 對話區域 */}
              <div className="col-span-1 bg-white rounded-xl p-6 shadow-lg">
                {/* SmartUI 對話區域對齊狀態指示 */}
                {smartUIActive && !dialogAligned && (
                  <div className="flex items-center justify-center space-x-2 mb-4">
                    <Zap className="w-4 h-4 text-purple-600 animate-pulse" />
                    <span className="text-sm text-purple-600">SmartUI 正在調整對話區域位置...</span>
                  </div>
                )}

                {/* SmartUI 部署狀態卡片添加指示 */}
                {smartUIActive && !deploymentCardAdded && dialogAligned && (
                  <div className="flex items-center justify-center space-x-2 mb-4">
                    <Rocket className="w-4 h-4 text-green-600 animate-pulse" />
                    <span className="text-sm text-green-600">SmartUI 正在添加部署狀態卡片...</span>
                  </div>
                )}

                {/* 對話框標題 */}
                <div className="flex items-center space-x-3 mb-4 pb-3 border-b border-gray-100">
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                    <MessageCircle className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-800">AI 智慧助手</h3>
                    <p className="text-sm text-gray-500">PowerAutomation 對話</p>
                  </div>
                  <div className="ml-auto flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-xs text-green-600">在線</span>
                  </div>
                </div>
                
                {/* 對話消息區域 */}
                <div className="space-y-4 mb-6 max-h-80 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100">
                  {messages.map((message) => (
                    <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-sm px-4 py-3 rounded-2xl shadow-sm ${
                        message.type === 'user' 
                          ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-br-md' 
                          : 'bg-gray-50 text-gray-800 rounded-bl-md border border-gray-200'
                      }`}>
                        {message.type === 'ai' && (
                          <div className="flex items-center space-x-2 mb-2">
                            <div className="w-5 h-5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
                              AI
                            </div>
                            <span className="text-xs text-gray-500">
                              {message.timestamp.toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit' })}
                            </span>
                          </div>
                        )}
                        {message.type === 'user' && (
                          <div className="flex items-center justify-end space-x-2 mb-2">
                            <span className="text-xs text-white/70">
                              {message.timestamp.toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit' })}
                            </span>
                            <div className="w-5 h-5 bg-white/20 rounded-full flex items-center justify-center text-white text-xs font-bold">
                              您
                            </div>
                          </div>
                        )}
                        <p className="text-sm leading-relaxed">{message.content}</p>
                      </div>
                    </div>
                  ))}
                  
                  {/* 正在輸入指示器 */}
                  <div className="flex justify-start">
                    <div className="bg-gray-50 border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
                      <div className="flex items-center space-x-2">
                        <div className="w-5 h-5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
                          AI
                        </div>
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* SmartUI 智慧感知輸入區域 */}
                <div className="border-t border-gray-100 pt-4">
                  <div className={`transition-all duration-1000 ${
                    inputOptimized ? 'flex space-x-3' : 'flex space-x-3'
                  }`}>
                    <div className="flex-1 relative">
                      <input
                        type="text"
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                        placeholder="輸入您的問題或需求..."
                        className={`w-full px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 ${
                          inputOptimized 
                            ? 'text-base py-4 shadow-md border-2 border-blue-300 bg-blue-50/30' 
                            : 'text-sm bg-gray-50'
                        }`}
                      />
                      {/* 輸入提示 */}
                      <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-2">
                        <div className="text-xs text-gray-400">Enter 發送</div>
                      </div>
                    </div>
                    
                    {/* SmartUI 智慧感知：條件顯示按鈕 */}
                    {!inputOptimized && (
                      <>
                        <button className="px-3 py-2 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors text-sm">
                          Manus
                        </button>
                        <button className="px-3 py-2 bg-purple-500 text-white rounded-xl hover:bg-purple-600 transition-colors text-sm">
                          應用
                        </button>
                        <button className="px-3 py-2 bg-green-500 text-white rounded-xl hover:bg-green-600 transition-colors text-sm">
                          飛書
                        </button>
                      </>
                    )}
                    
                    <button 
                      onClick={handleSendMessage}
                      disabled={!inputMessage.trim()}
                      className={`bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-2xl hover:from-purple-600 hover:to-pink-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed ${
                        inputOptimized 
                          ? 'px-6 py-4 shadow-lg transform hover:scale-105' 
                          : 'px-4 py-3'
                      }`}
                    >
                      <Send className={`transition-all duration-300 ${
                        inputOptimized ? 'w-5 h-5' : 'w-4 h-4'
                      }`} />
                    </button>
                  </div>
                  
                  {/* 快捷回覆建議 */}
                  <div className="mt-3 flex flex-wrap gap-2">
                    <button 
                      onClick={() => setInputMessage('查看系統狀態')}
                      className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full text-xs transition-colors"
                    >
                      查看系統狀態
                    </button>
                    <button 
                      onClick={() => setInputMessage('開始新的工作流')}
                      className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full text-xs transition-colors"
                    >
                      開始新的工作流
                    </button>
                    <button 
                      onClick={() => setInputMessage('檢查部署狀態')}
                      className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full text-xs transition-colors"
                    >
                      檢查部署狀態
                    </button>
                  </div>
                </div>
              </div>
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {message.type === 'ai' && (
                          <div className="flex items-center space-x-2 mb-2">
                            <div className="w-6 h-6 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
                              AI
                            </div>
                          </div>
                        )}
                        <p className="text-sm">{message.content}</p>
                      </div>
                    </div>
                  ))}
                </div>

                {/* SmartUI 智慧感知輸入區域 */}
                <div className={`transition-all duration-1000 ${
                  inputOptimized ? 'flex space-x-2' : 'flex space-x-3'
              }`}>
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="描述您的開發需求，AI將智能介入協助..."
                  className={`px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-1000 ${
                    inputOptimized 
                      ? 'flex-1 text-lg py-4 shadow-lg border-2 border-blue-300' 
                      : 'flex-1'
                  }`}
                />
                
                {/* SmartUI 智慧感知：條件顯示按鈕 */}
                {!inputOptimized && (
                  <>
                    <button className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors opacity-100 transform scale-100">
                      Manus
                    </button>
                    <button className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors opacity-100 transform scale-100">
                      應用
                    </button>
                    <button className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors opacity-100 transform scale-100">
                      飛書
                    </button>
                  </>
                )}
                
                <button 
                  onClick={handleSendMessage}
                  className={`bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all duration-1000 ${
                    inputOptimized 
                      ? 'px-6 py-4 text-lg shadow-lg transform hover:scale-105' 
                      : 'px-4 py-2'
                  }`}
                >
                  <Send className={`transition-all duration-1000 ${
                    inputOptimized ? 'w-5 h-5' : 'w-4 h-4'
                  }`} />
                </button>
              </div>
              </div>
              
              {/* 部署狀態卡片 */}
              <div className={`col-span-1 transition-all duration-1000 ${
                deploymentCardAdded ? 'opacity-100 transform translate-y-0' : 'opacity-0 transform translate-y-4'
              }`}>
                <div className="bg-gradient-to-br from-green-50 to-emerald-100 rounded-xl p-6 shadow-lg border border-green-200">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center">
                        <Rocket className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-green-800">部署狀態</h3>
                        <p className="text-sm text-green-600">實時監控</p>
                      </div>
                    </div>
                    <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                  </div>
                  
                  {/* 部署進度 */}
                  <div className="space-y-3 mb-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-green-700">部署進度</span>
                      <span className="text-sm font-bold text-green-800">85%</span>
                    </div>
                    <div className="w-full bg-green-200 rounded-full h-2">
                      <div className="bg-gradient-to-r from-green-500 to-emerald-500 h-2 rounded-full" style={{ width: '85%' }}></div>
                    </div>
                  </div>

                  {/* 服務狀態 */}
                  <div className="space-y-2 mb-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span className="text-sm text-green-700">前端服務</span>
                      </div>
                      <span className="text-xs bg-green-500 text-white px-2 py-1 rounded">運行中</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span className="text-sm text-green-700">後端 API</span>
                      </div>
                      <span className="text-xs bg-green-500 text-white px-2 py-1 rounded">運行中</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Clock className="w-4 h-4 text-yellow-600" />
                        <span className="text-sm text-green-700">資料庫</span>
                      </div>
                      <span className="text-xs bg-yellow-500 text-white px-2 py-1 rounded">連接中</span>
                    </div>
                  </div>

                  {/* 部署統計 */}
                  <div className="grid grid-cols-2 gap-3 text-center">
                    <div className="bg-white/50 rounded-lg p-3">
                      <div className="text-lg font-bold text-green-800">12</div>
                      <div className="text-xs text-green-600">成功部署</div>
                    </div>
                    <div className="bg-white/50 rounded-lg p-3">
                      <div className="text-lg font-bold text-green-800">2.3s</div>
                      <div className="text-xs text-green-600">平均響應</div>
                    </div>
                  </div>

                  {/* 最近部署 */}
                  <div className="mt-4 pt-3 border-t border-green-200">
                    <div className="text-xs text-green-600 mb-2">最近部署</div>
                    <div className="space-y-1">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-green-700">v1.2.3</span>
                        <span className="text-green-600">2分鐘前</span>
                      </div>
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-green-700">v1.2.2</span>
                        <span className="text-green-600">1小時前</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* SmartUI 智慧感知橫向三節點工作流 */}
            <div className="bg-white rounded-xl p-6 shadow-lg">
              {/* SmartUI 狀態指示器 */}
              {smartUIActive && !layoutOptimized && (
                <div className="flex items-center justify-center space-x-2 mb-4">
                  <Zap className="w-4 h-4 text-blue-600 animate-pulse" />
                  <span className="text-sm text-blue-600">SmartUI 優化中...</span>
                </div>
              )}
              
              {smartUIActive && layoutOptimized && !inputOptimized && (
                <div className="flex items-center justify-center space-x-2 mb-4">
                  <Zap className="w-4 h-4 text-orange-600 animate-pulse" />
                  <span className="text-sm text-orange-600">SmartUI 正在優化輸入體驗...</span>
                </div>
              )}

              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-800 mb-2">三節點工作流</h3>
              </div>
              
              {/* 橫向三節點按鈕 - SmartUI 智慧感知佈局 */}
              <div className={`transition-all duration-1000 ${
                layoutOptimized 
                  ? 'flex space-x-2' 
                  : 'grid grid-cols-1 gap-4'
              }`}>
                <button 
                  onClick={() => handleNodeClick('coding')}
                  className={`bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 flex items-center justify-center space-x-2 relative ${
                    layoutOptimized ? 'flex-1 h-16' : 'h-12'
                  } ${nodeStates.coding.status === 'running' ? 'animate-pulse' : ''}`}
                >
                  <Code className={`${layoutOptimized ? 'w-6 h-6' : 'w-5 h-5'}`} />
                  <span className={`font-semibold ${layoutOptimized ? 'text-lg' : 'text-base'}`}>編碼</span>
                  {nodeStates.coding.status === 'completed' && (
                    <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full flex items-center justify-center">
                      <CheckCircle className="w-3 h-3 text-white" />
                    </div>
                  )}
                  <div className="absolute bottom-1 right-2 text-xs opacity-75">
                    {nodeStates.coding.progress}%
                  </div>
                </button>
                
                <button 
                  onClick={() => handleNodeClick('testing')}
                  className={`bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 flex items-center justify-center space-x-2 relative ${
                    layoutOptimized ? 'flex-1 h-16' : 'h-12'
                  } ${nodeStates.testing.status === 'running' ? 'animate-pulse' : ''}`}
                >
                  <Edit className={`${layoutOptimized ? 'w-6 h-6' : 'w-5 h-5'}`} />
                  <span className={`font-semibold ${layoutOptimized ? 'text-lg' : 'text-base'}`}>測試</span>
                  {nodeStates.testing.status === 'completed' && (
                    <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full flex items-center justify-center">
                      <CheckCircle className="w-3 h-3 text-white" />
                    </div>
                  )}
                  <div className="absolute bottom-1 right-2 text-xs opacity-75">
                    {nodeStates.testing.progress}%
                  </div>
                </button>
                
                <button 
                  onClick={() => handleNodeClick('deployment')}
                  className={`bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 flex items-center justify-center space-x-2 relative ${
                    layoutOptimized ? 'flex-1 h-16' : 'h-12'
                  } ${nodeStates.deployment.status === 'deploying' ? 'animate-pulse' : ''}`}
                >
                  <Rocket className={`${layoutOptimized ? 'w-6 h-6' : 'w-5 h-5'}`} />
                  <span className={`font-semibold ${layoutOptimized ? 'text-lg' : 'text-base'}`}>部署</span>
                  {nodeStates.deployment.status === 'completed' && (
                    <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full flex items-center justify-center">
                      <CheckCircle className="w-3 h-3 text-white" />
                    </div>
                  )}
                  <div className="absolute bottom-1 right-2 text-xs opacity-75">
                    {nodeStates.deployment.progress}%
                  </div>
                </button>
              </div>
            </div>
          </div>

          {/* 右側統計和快捷操作 */}
          <div className="col-span-3 space-y-4">
            {/* 編碼工作流統計 */}
            <div className="bg-gradient-to-br from-blue-100 to-blue-200 rounded-xl p-4 shadow-lg">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <Code className="w-4 h-4 text-white" />
                </div>
                <span className="font-semibold text-blue-800">編碼工作流</span>
              </div>
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-blue-800">100</div>
                  <div className="text-xs text-blue-600">代碼質量</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-blue-800">92</div>
                  <div className="text-xs text-blue-600">架構合規</div>
                </div>
              </div>
            </div>

            {/* 測試工作流統計 */}
            <div className="bg-gradient-to-br from-orange-100 to-orange-200 rounded-xl p-4 shadow-lg">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-8 h-8 bg-orange-600 rounded-lg flex items-center justify-center">
                  <Edit className="w-4 h-4 text-white" />
                </div>
                <span className="font-semibold text-orange-800">測試工作流</span>
              </div>
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-orange-800">85</div>
                  <div className="text-xs text-orange-600">覆蓋率%</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-orange-800">3</div>
                  <div className="text-xs text-orange-600">測試用例</div>
                </div>
              </div>
            </div>

            {/* 部署工作流統計 */}
            <div className="bg-gradient-to-br from-green-100 to-green-200 rounded-xl p-4 shadow-lg">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
                  <Rocket className="w-4 h-4 text-white" />
                </div>
                <span className="font-semibold text-green-800">部署工作流</span>
              </div>
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-green-800">12</div>
                  <div className="text-xs text-green-600">成功部署</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-green-800">2.3s</div>
                  <div className="text-xs text-green-600">平均時間</div>
                </div>
              </div>
            </div>

            {/* 系統監控 */}
            <div className="bg-gradient-to-br from-purple-100 to-purple-200 rounded-xl p-4 shadow-lg">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                  <Activity className="w-4 h-4 text-white" />
                </div>
                <span className="font-semibold text-purple-800">系統監控</span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-purple-700">CPU 使用率</span>
                  <span className="text-sm font-bold text-purple-800">45%</span>
                </div>
                <div className="w-full bg-purple-200 rounded-full h-2">
                  <div className="bg-purple-500 h-2 rounded-full" style={{ width: '45%' }}></div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-purple-700">記憶體使用</span>
                  <span className="text-sm font-bold text-purple-800">68%</span>
                </div>
                <div className="w-full bg-purple-200 rounded-full h-2">
                  <div className="bg-purple-500 h-2 rounded-full" style={{ width: '68%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

