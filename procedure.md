# 📘 daTEAbase 專案工作 Procedure（團隊版）

> 本專案採用 PostgreSQL + Python（Console UI） 架構  
> 採嚴格分層設計，確保可維護性與多人協作安全  
> 本文件說明系統架構、分層職責、開發規範與協作流程  
> （與 ChatGPT 協作整理）    

---

## 一、專案整體設計理念

### ✅ 四層分離原則
```css
menu (流程選單)
↓
UI（使用者輸入／顯示）
↓
DB（所有 SQL 與資料操作）
↓
PostgreSQL（實際資料庫）
```

### ✅ 各層責任
- **menu 層**：控制流程與選單跳轉
- **UI 層**：`input()`、`print()`、格式驗證、呼叫 DB function  
- **DB 層**：CRUD、SQL、`commit / rollback`  
- **DB 本體**：純資料儲存

### 🚫 嚴格禁止事項
- 在 menu 定義業務邏輯(UI function)
- 在 UI 裡寫 raw SQL  
- UI 直接 `cursor.execute()`  
- DB 層讀 `input()`


---

## 二、資料夾結構與職責
```pgsql
DB_114-1_g27/
│
├─ db/ ← ✅ 資料庫層
│ ├─ conn.py ← DB 連線、commit、rollback
│ ├─ common.py ← 通用 CRUD（insert / update / fetch / exists）
│ ├─ allowed.py ← 白名單（防 SQL injection）
│ ├─ user/ ← user 相關 DB function (Optional:若有其他helper function需要定義，可在該子資料夾創helper.py)
│ └─ 其他功能待補(請新增folder如custromer, brand, admin, etc.並將相關function置入其中)
|
├─ ui/ ← ✅ 使用者介面層
│ ├─ helper.py ← cancel_check 等共用工具
│ ├─ main.py ← UI 進入點（顯示選單）
│ ├─ user/ ← login / create user UI
| └─ 其他功能待補
│
├─ menu/ ← ✅ 選單流程控制
│ ├─ main_menu.py
| └─ 其他子流程待補
│
├─ schema/ ← ✅ DB 初始化 SQL（模組化）
│ ├─ 001_init_mod1.sql
│ ├─ 002_init_mod2.sql
│ ├─ 003_init_mod3.sql
│ └─ 004_init_mod4.sql
|
├─ daTEAbase.backup (DB備份檔)
├─ main.py ← 專案啟動入口
├─ procedure.md
└─ README.md
```


---

## 三、如何連線本地 PostgreSQL（每個人都要做）

### 1️⃣ 安裝必要套件
```bash
pip install psycopg2-binary python-dotenv
```

### 2️⃣ 建立 .env（不要 commit）
在專案 root 建立 .env：
```env
DB_PASSWORD=你的postgres密碼
```
⚠️ 不要有空格或引號  
.env會被.gitignore忽略，其他人無法存取你的本地postgre密碼

### 3️⃣ 初始化資料庫
1. 使用 pgAdmin / psql 建立資料庫：
   ```nginx
   daTEAbase
   ```
2. 依序執行：
   ```pgsql
   schema/001_init_mod1.sql
   schema/002_init_mod2.sql
   schema/003_init_mod3.sql
   schema/004_init_mod4.sql
   ```
   ⚠️ schema SQL 必須依照檔名前綴順序執行，否則 foreign key 會失敗

**(待db資料匯入後將改為下載.backup並匯入本地)**

### 4️⃣ 資料庫連線方式

因 db.common 已經處理所有需要與資料庫連線之SQL，所有 DB function 檔案需要 import
```python
from db.common import insert, fetch, delete, exists, update
```
資料庫連線由 main.py 統一負責呼叫 connect()，DB 層函式不得自行連線。

## 四、DB 層開發規範
### ✅ DB 層只能做資料操作（NO UI），所有 DB 操作也只能寫在 DB 層

建議結構範例：
```
db/user/create.py
db/store/create.py
db/order/create.py
```

✅ CRUD 一律使用 db.common
範例：
```python
insert("APP_USER", {...})
update("STORE", {...}, {"store_id": 1})
fetch("PRODUCT", {"brand_id": 2})
exists("STORE", {"store_id": 5})
```
⚠️ 表名必須大寫，欄位名必需小寫

🚫 DB 層禁止事項
- 禁止 input()
- 禁止 print()
- 禁止 DB 內自行 connect
- 禁止 UI 驗證邏輯

## 五、UI 層開發規範
UI 只負責三件事：
1. input()
2. 基本驗證（格式 / :q 取消）
3. 呼叫 DB function

✅ 回傳 id / status  
✅ 建議任何 input 後都 check_cancel() 一次 （詳見 ui.helper ）
🚫 不直接處理 DB row  
🚫 不寫 SQL

## 六、import 規範（避免 ModuleNotFoundError）
✅ import 範例
```python
from db.user.create import db_create_user
from ui.helper import cancel_check
```

✅ 若要實際操作，一律從 root 啟動：
```bash
python main.py
```
❌ 不要直接執行子資料夾檔案
 

## 七、命名規範
### 資料夾名
- 依照該資料夾功能命名
- 創建資料夾後，請再該子資料夾同步創建
  ```python
  __init__.py
  ```
  以確保 import 順利
  
### 檔名
- xxx.py → DB / UI function
- *_menu.py → 選單流程

### 檔案內def function
- DB層範例：
  ```python
  db_create_user()
  db_login_user()

  db_create_brand()
  db_create_store()
  db_update_store_info()

  db_create_order()
  db_add_order_item()
  ```
- UI層範例：
  ```python
  ui_create_user()
  ui_login_user()

  ui_create_store()
  ui_set_store_hours()
  ```
  (若為 helper function 且確定不會 override，可選擇不加前綴)
⚠️ 為防止override ， DB 層與 UI 層 function 不得使用相同名稱，
例如：請使用 db_create_user() 與 ui_create_user()
  
### SQL 檔案
```python
001_init_mod1.sql
002_init_mod2.sql
```
（依模組順序）

## 八、團隊協作
每人只動自己模組的 db/ 與 ui/，避免內容覆寫。

