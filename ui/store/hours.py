
from db.store.hours import (
    db_fetch_store_hours,
    db_update_store_hours
)
from ui.helper import clear_screen, cancel_check

# 中文對齊輔助函數
def get_display_width(text):
    """計算字串顯示寬度（中文字算2個字元，英文算1個）"""
    width = 0
    for char in str(text):
        if '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303f':
            width += 2
        else:
            width += 1
    return width

def pad_string(text, target_width):
    """將字串填充到指定顯示寬度"""
    current_width = get_display_width(text)
    padding = target_width - current_width
    return text + ' ' * max(0, padding)


def ui_view_store_hours(store_id):
    """查看門市營業時間"""
    clear_screen()
    print("\n=== 門市營業時間 ===\n")
    
    try:
        hours = db_fetch_store_hours(store_id)
        
        if not hours:
            print("⚠️ 此門市尚未設定營業時間")
            return hours
        
        weekday_names = ["週日", "週一", "週二", "週三", "週四", "週五", "週六"]
        
        print(f"{pad_string('星期', 12)}{pad_string('營業狀態', 16)}{pad_string('營業時間', 24)}")
        print("="*52)
        
        for hour in hours:
            weekday_name = weekday_names[hour['weekday']]
            status = "✅ 營業" if hour['is_open'] else "❌ 公休"
            
            if hour['is_open'] and hour['open_time'] and hour['close_time']:
                # 格式化時間（去掉秒數）
                open_time = str(hour['open_time'])[:5]
                close_time = str(hour['close_time'])[:5]
                time_str = f"{open_time} - {close_time}"
            else:
                time_str = "—"
            
            print(f"{pad_string(weekday_name, 12)}{pad_string(status, 16)}{pad_string(time_str, 24)}")
        
        return hours
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def ui_update_store_hours(store_id):
    """更新門市營業時間"""
    clear_screen()
    print("\n=== 更新門市營業時間 ===\n")
    
    try:
        # 先顯示目前營業時間
        hours = ui_view_store_hours(store_id)
        
        if not hours:
            print("\n⚠️ 請先初始化營業時間")
            return
        
        weekday_names = ["週日", "週一", "週二", "週三", "週四", "週五", "週六"]
        
        # 選擇要修改的星期
        print("\n請選擇要修改的星期：")
        for i, name in enumerate(weekday_names):
            print(f"{i}. {name}")
        print("q. 返回")
        
        choice = input("\n請輸入選項 (0-6): ").strip()
        
        if choice.lower() == 'q':
            return
        
        try:
            weekday = int(choice)
            if not (0 <= weekday <= 6):
                print("❌ 無效的選項")
                return
        except ValueError:
            print("❌ 無效的選項")
            return
        
        # 取得該日目前資訊
        current = next((h for h in hours if h['weekday'] == weekday), None)
        
        if not current:
            print("❌ 找不到該日資料")
            return
        
        clear_screen()
        print(f"\n=== 更新 {weekday_names[weekday]} 營業時間 ===\n")
        print(f"目前狀態：{'✅ 營業' if current['is_open'] else '❌ 公休'}")
        
        if current['is_open']:
            open_time = str(current['open_time'])[:5] if current['open_time'] else "未設定"
            close_time = str(current['close_time'])[:5] if current['close_time'] else "未設定"
            print(f"目前時間：{open_time} - {close_time}")
        
        print()
        
        updates = {}
        
        # 營業狀態
        print("營業狀態：")
        print("1. 營業")
        print("2. 公休")
        status_choice = input("選擇（留空不變）: ").strip()
        
        if status_choice == "1":
            updates["is_open"] = True
            
            # 如果改為營業，需要設定營業時間
            print("\n營業時間（格式：HH:MM，例如 10:00）")
            
            open_time = input(f"開始時間 [{str(current['open_time'])[:5] if current['open_time'] else '10:00'}]: ").strip()
            if open_time:
                if not validate_time_format(open_time):
                    print("❌ 時間格式錯誤")
                    return
                updates["open_time"] = f"{open_time}:00"
            
            close_time = input(f"結束時間 [{str(current['close_time'])[:5] if current['close_time'] else '22:00'}]: ").strip()
            if close_time:
                if not validate_time_format(close_time):
                    print("❌ 時間格式錯誤")
                    return
                updates["close_time"] = f"{close_time}:00"
        
        elif status_choice == "2":
            updates["is_open"] = False
            updates["open_time"] = None
            updates["close_time"] = None
        
        # 如果沒有要更新的欄位
        if not updates:
            print("⚠️ 沒有要更新的欄位")
            return
        
        # 確認更新
        print("\n確認更新：")
        if "is_open" in updates:
            print(f"  營業狀態：{'營業' if updates['is_open'] else '公休'}")
        if "open_time" in updates and updates["open_time"]:
            print(f"  開始時間：{updates['open_time'][:5]}")
        if "close_time" in updates and updates["close_time"]:
            print(f"  結束時間：{updates['close_time'][:5]}")
        
        confirm = input("\n確認更新？(y/n): ").strip().lower()
        
        if confirm == 'y':
            db_update_store_hours(store_id, weekday, **updates)
            print(f"\n✅ {weekday_names[weekday]} 營業時間更新成功")
        else:
            print("❌ 操作已取消")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def validate_time_format(time_str):
    """驗證時間格式（HH:MM）"""
    try:
        parts = time_str.split(':')
        if len(parts) != 2:
            return False
        
        hour = int(parts[0])
        minute = int(parts[1])
        
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            return False
        
        return True
    except:
        return False


def ui_batch_update_store_hours(store_id):
    """批次更新營業時間（一次設定所有星期）"""
    clear_screen()
    print("\n=== 批次更新營業時間 ===\n")
    print("此功能可一次設定週一到週日的營業時間\n")
    
    try:
        # 輸入營業時間
        print("營業時間（格式：HH:MM，例如 10:00）")
        open_time = input("開始時間: ").strip()
        
        if not validate_time_format(open_time):
            print("❌ 時間格式錯誤")
            return
        
        close_time = input("結束時間: ").strip()
        
        if not validate_time_format(close_time):
            print("❌ 時間格式錯誤")
            return
        
        # 選擇公休日
        print("\n請選擇公休日（可多選，用逗號分隔，例如：0,6 表示週日和週六）")
        print("0=週日, 1=週一, 2=週二, 3=週三, 4=週四, 5=週五, 6=週六")
        print("（留空表示全週營業）")
        
        closed_days_input = input("公休日: ").strip()
        
        if closed_days_input:
            try:
                closed_days = [int(x.strip()) for x in closed_days_input.split(',')]
                if not all(0 <= d <= 6 for d in closed_days):
                    print("❌ 無效的星期代碼")
                    return
            except ValueError:
                print("❌ 格式錯誤")
                return
        else:
            closed_days = []
        
        # 確認更新
        weekday_names = ["週日", "週一", "週二", "週三", "週四", "週五", "週六"]
        
        print("\n確認批次更新：")
        print(f"營業時間：{open_time} - {close_time}")
        
        if closed_days:
            closed_names = [weekday_names[d] for d in closed_days]
            print(f"公休日：{', '.join(closed_names)}")
        else:
            print("公休日：無（全週營業）")
        
        confirm = input("\n確認更新？(y/n): ").strip().lower()
        
        if confirm == 'y':
            count = 0
            for weekday in range(7):
                if weekday in closed_days:
                    updates = {
                        "is_open": False,
                        "open_time": None,
                        "close_time": None
                    }
                else:
                    updates = {
                        "is_open": True,
                        "open_time": f"{open_time}:00",
                        "close_time": f"{close_time}:00"
                    }
                
                try:
                    db_update_store_hours(store_id, weekday, **updates)
                    count += 1
                except Exception as e:
                    print(f"❌ 更新 {weekday_names[weekday]} 失敗: {e}")
            
            print(f"\n✅ 批次更新完成（成功更新 {count}/7 天）")
        else:
            print("❌ 操作已取消")
    
    except Exception as e:
        print(f"❌ Error: {e}")
