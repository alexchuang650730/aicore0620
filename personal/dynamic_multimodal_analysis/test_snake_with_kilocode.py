#!/usr/bin/env python3
"""
直接使用KiloCode引擎開發貪吃蛇遊戲
"""

import sys
import json
import asyncio
from pathlib import Path

# 添加路徑
sys.path.append('/tmp/aicore0619')
sys.path.append('/home/ubuntu/enterprise_deployment')

async def test_snake_game_with_kilocode():
    """使用KiloCode引擎開發貪吃蛇遊戲"""
    
    try:
        print("🚀 啟動KiloCode引擎...")
        from mcp.adapter.kilocode_mcp.kilocode_mcp import KiloCodeMCP
        
        # 初始化KiloCode
        kilocode = KiloCodeMCP()
        print("✅ KiloCode引擎初始化成功")
        
        # 準備貪吃蛇遊戲需求
        game_request = {
            "action": "create_game",
            "game_type": "snake_game",
            "content": "开发一个Python贪吃蛇游戏，包含游戏逻辑、图形界面和计分系统",
            "requirements": {
                "name": "貪吃蛇遊戲",
                "description": "開發一個Python貪吃蛇遊戲",
                "features": [
                    "基本的貪吃蛇遊戲邏輯",
                    "圖形界面（使用pygame）",
                    "鍵盤控制（方向鍵）",
                    "計分系統",
                    "遊戲結束判斷",
                    "食物生成機制"
                ],
                "technology": "Python + pygame",
                "complexity": "medium"
            }
        }
        
        print("\n📋 遊戲開發需求:")
        print(json.dumps(game_request, indent=2, ensure_ascii=False))
        
        # 調用KiloCode處理請求
        print("\n🔄 KiloCode處理中...")
        result = await kilocode.process_request(game_request)
        
        print("\n✅ KiloCode處理結果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 如果有生成的代碼，保存並顯示到文件
        if result.get("success") and "content" in result:
            output_dir = Path("/home/ubuntu/enterprise_deployment/snake_game_output")
            output_dir.mkdir(exist_ok=True)
            
            code_file = output_dir / "snake_game.py"
            with open(code_file, 'w', encoding='utf-8') as f:
                f.write(result["content"])
            
            print(f"\n💾 代碼已保存到: {code_file}")
            print(f"📝 代碼預覽（前20行）:")
            print("=" * 50)
            lines = result["content"].split('\n')
            for i, line in enumerate(lines[:20], 1):
                print(f"{i:2d}: {line}")
            if len(lines) > 20:
                print(f"... (還有 {len(lines) - 20} 行)")
            print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_snake_game_with_kilocode())
    if success:
        print("\n🎉 貪吃蛇遊戲開發測試完成！")
    else:
        print("\n❌ 貪吃蛇遊戲開發測試失敗")

