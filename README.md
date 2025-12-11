# 114-1 資料庫管理 - DaTEAbase 專案

## 專案簡介

在經營手搖飲品牌的路上，最讓人頭痛的，從來不是「茶要不要加冰」，而是系統各自為政、資料七零八落、訂單和庫存永遠對不起來。如果你也有這些困擾，就來認識 daTEAbase 吧。

daTEAbase 是一個專為手搖飲與連鎖餐飲打造的營運管理平台，支援「多品牌、多門市」的集團式架構、商品客製化、即時庫存連動、從下單到評分的完整訂單流程，讓經營回到該有的順手與清醒。

## 使用者功能

### User （一般使用者）

#### 使用者登入、註冊

- 註冊：使用者可以註冊帳號設定使用者名稱、電話、密碼及電子郵件信箱，系統會分配一個 user_id 給每位使用者。
- 登入：使用電話號碼登入並驗證密碼。

#### 管理個人帳號資訊

- 使用者可以修改自己的使用者名稱、密碼及電子郵件信箱。
- 使用者可以新增和修改個人常用外送地址。

#### 瀏覽特定店家的商品菜單

- 使用者可以選擇品牌及店家，並瀏覽該店的菜單。

#### 建立訂單

- 訂單類型：使用者可以選擇自取或外送。
- 客製化：使用者可以選擇店家的特定商品與數量，並根據商家制定的規則進行客製化調整。

#### 評價訂單

- 使用者可以針對已完成的訂單及訂單商品提交評分與評論。

### Store Staff (店家員工)

除了上述 User 擁有的功能以外，還增加以下功能：

#### 管理門市資訊

- 基本資訊：修改營業時間、設定外送門檻、開啟或關閉接單狀態。
- 門市商品：設定商品販售價格與上架狀態。
- 門市選項：停用或啟用特定客製化選項（例如珍珠售完時停用該選項）。

#### 訂單查詢與管理

- 店員可以查看門市的新訂單並操作訂單狀態，包含「接受訂單」和「完成訂單」。
-  查看訂單明細及其客製化選項以便備餐。

### Brand Manager (品牌管理員)

除了上述 User 擁有的功能以外，還增加以下功能：

#### 商品管理

- 管理員可以新增、修改特定品項的資料。
- 管理員可以啟用或停用該品項。

#### 客製化選項管理

- 管理員可以新增或修改選項群組（如甜度、冰塊、加料）或特定選項的資料。
- 管理員可以啟用或停用選項群組或特定選項。
- 管理員可以綁定每個商品適用的選項群組規則（下單該商品時，至少／至多需選擇幾個選項）
- 管理員可以設定選項的互斥邏輯（例如冰沙不適用「熱飲」）

## 使用方法

1. 建立資料庫並依序執行 `./intialization` 資料夾內的檔案：
``` psql
CREATE DATABASE daTEAbase;

psql -U postgres -d databaseproject -f ./intialization/001_init_schema_mod1.sql
psql -U postgres -d databaseproject -f ./intialization/002_init_schema_mod2.sql
psql -U postgres -d databaseproject -f ./intialization/003_init_schema_mod3.sql
psql -U postgres -d databaseproject -f ./intialization/004_init_reset_database.sql
psql -U postgres -d databaseproject -f ./intialization/005_init_test_data_new.sql
```

2. 在 `db_conn.py` 設定**資料庫名稱** (DB_NAME)、**使用者名稱** (DB_USER)、**主機位置** (DB_HOST)及**通訊埠** (DB_PORT)。
3. 在 `./`(root) 建立 `.env`：
    ```env
    DB_PASSWORD=你的postgres密碼
    ```
    **⚠️不要有空格或引號**  (註：`.env` 會被 `.gitignore` 忽略，本地 postgres 密碼不會被 git 存取)
    
4. 最後，執行 `main.py` 來啟動系統：
   ```bash
   python .\main.py
   ```

建議用以下帳號來測試不同身分的使用者：
- 一般使用者：電話：0911111111、密碼：aaa111。
- 店家員工：電話：0945678901、密碼：staff123。
- 品牌管理員：電話：0956789012、密碼：manager123。

## 技術細節

- 資料庫使用 PostgreSQL，使用套件 Psycopg2 對資料庫進行操作

- **交易管理**：本系統於 `./db/conn.py` 中將資料庫連線設定為 `autocommit = False`，確保所有資料庫操作皆預設在交易（Transaction）中執行。基本的 CRUD 函式（如 `insert`、`update`、`delete` ）若遇到錯誤，會自動呼叫 `db.rollback()`撤回此次交易（其中 `db` 為 Psycopg2 的 connection 物件，負責資料庫連線），以取消先前所有尚未提交的資料庫異動。由於本系統各功能模組普遍引用基礎 CRUD 函式，因此自然繼承了上述交易管理機制。

    - 可參考： `./db/crud.py`

- **併行控制**：針對【更新訂單狀態】功能，為避免不同店員對訂單進行不同操作或顧客取消訂單時被接受，造成資料衝突，在使用者對狀態為 `placed` 的訂單按下確定更改相關資訊時，系統會針對此訂單加鎖，更改狀態為 `accepted`、`rejected` 或 `canceled` 後並且解鎖。

  - 可參考 `./db/crud.py` 中的 `lock_rows()`、`./db/tx.py` 以及 `./db/order/manage.py 中的  `db_accept_order()`、`db_reject_order()` 和 `db_cancel_order()`。

  

## 程式說明

1. **`./main.py`**
   - 系統執行入口，負責呼叫連線功能和主流程。
2. **`./db`** 資料夾
   -  封裝與資料庫相關的功能，包含資料庫連線管理與查詢操作。
3. **`./ui`** 資料夾
   -  管理 UI 介面操作並呼叫 DB 程式完成功能。
   -  程式具備高度擴展性，開發者可透過新增子資料夾類別或子程式輕鬆增加新功能。
4. **`./menu`** 資料夾
   - 與流程控制相關的功能。
   - 顯示相關選單，待使用者輸入指令後進入子流程選單或呼叫相關 UI 程式。



## 開發環境

- Windows 11
  
- Python: 3.11
  
  - psycopg2
    
  - python-dotenv
    
  - bcrypt
 
  - pymongo
    
- PostgreSQL: 17.6

- MongoDB: 8.2
