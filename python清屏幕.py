import os

def clear_screen():
    """根據作業系統清空終端機畫面。"""
    # 判斷作業系統
    if os.name == 'posix':  # Linux and macOS
        os.system('clear')
    else:  # Windows
        os.system('cls')

# --- 使用範例 ---
print("這是清屏前的內容...")
input("按 Enter 鍵清屏...") # 等待用戶操作
clear_screen() # 執行清屏
print("這是在清屏後顯示的內容！")
