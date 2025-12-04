# 📘 daTEAbase 專案工作 Procedure（團隊版）

> 本專案為「飲料店下單／庫存／分析系統」  
> 採 **PostgreSQL + Python（Console UI）** 架構  
> 本文件說明整體分層邏輯、資料夾責任分工，以及各組員如何接續實作

---

## 一、專案整體設計理念

### ✅ 四層分離原則
menu (console選項流程)
↓
UI（使用者輸入／顯示）
↓
DB（所有 SQL 與資料操作）
↓
PostgreSQL（實際資料庫）

### ✅ 各層責任
- **menu 層**:使用流程
- **UI 層**：`input()`、`print()`、格式驗證、呼叫 DB function  
- **DB 層**：CRUD、SQL、`commit / rollback`  
- **DB 本體**：只存資料

### ⚠️ 嚴格禁止
- 在 menu 定義使用者功能
- 在 UI 裡寫 raw SQL  
- UI 直接 `cursor.execute()`  
- DB 層讀 `input()`


---

## 二、資料夾結構與職責
DB_114-1_g27/
│
├─ db/ ← ✅ 資料庫層
│ ├─ conn.py ← DB 連線、commit、rollback
│ ├─ common.py ← 通用 CRUD（insert / update / fetch / exists）
│ ├─ allowed.py ← 白名單（防 SQL injection）
│ ├─ user/ ← user 相關 DB function
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


---

## 三、如何連線本地 PostgreSQL（每個人都要做）

### 1️⃣ 安裝套件
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

3️⃣ 初始化資料庫
使用 postgresql 創建 daTEAbase後依序執行：
```pgsql
schema/001_init_mod1.sql
schema/002_init_mod2.sql
schema/003_init_mod3.sql
schema/004_init_mod4.sql
```
此後db的所有function只要有
```
from db.conn import db, cur
```
db.connect就會自動連接本地的資料庫(#會讀取.env)

