-- PRODUCT：商品
CREATE TABLE IF NOT EXISTS PRODUCT
(
    product_id           bigserial      NOT NULL,
    brand_id             bigint         NOT NULL,
    product_name         varchar(20)    NOT NULL,
    size                 varchar(10),
    product_description  varchar(100),
    image_url            varchar(100),
    is_active            boolean        NOT NULL DEFAULT true,
    created_at           timestamp      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at           timestamp      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PRODUCT_pkey PRIMARY KEY (product_id),
    CONSTRAINT PRODUCT_brand_id_fkey FOREIGN KEY (brand_id)
        REFERENCES BRAND(brand_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- STORE_PRODUCT：門市販售商品與價格
CREATE TABLE IF NOT EXISTS STORE_PRODUCT
(
    store_id     bigint        NOT NULL,
    product_id   bigint        NOT NULL,
    price        int           NOT NULL,
    is_active    boolean       NOT NULL DEFAULT true,
    created_at   timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT STORE_PRODUCT_pkey PRIMARY KEY (store_id, product_id),
    CONSTRAINT STORE_PRODUCT_store_id_fkey FOREIGN KEY (store_id)
        REFERENCES STORE(store_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT STORE_PRODUCT_product_id_fkey FOREIGN KEY (product_id)
        REFERENCES PRODUCT(product_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT STORE_PRODUCT_price_chk CHECK (price >= 0)
);

-- OPTION_CATEGORY：選項群組
CREATE TABLE IF NOT EXISTS OPTION_CATEGORY
(
    o_category_id      bigserial     NOT NULL,
    brand_id           bigint        NOT NULL,
    o_category_name    varchar(100)  NOT NULL,
    display_order      int,
    is_active          boolean       NOT NULL DEFAULT true,
    created_at         timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT OPTION_CATEGORY_pkey PRIMARY KEY (o_category_id),
    CONSTRAINT OPTION_CATEGORY_brand_id_fkey FOREIGN KEY (brand_id)
        REFERENCES BRAND(brand_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT OPTION_CATEGORY_display_order_chk
        CHECK (display_order IS NULL OR display_order >= 0)
);

-- OPTION：單一選項（加料／甜度冰塊等）
CREATE TABLE IF NOT EXISTS OPTION
(
    option_id       bigserial    NOT NULL,
    o_category_id   bigint       NOT NULL,
    option_name     varchar(20)  NOT NULL,
    price_adjust    int          NOT NULL DEFAULT 0
        CHECK (price_adjust >= -1000 AND price_adjust <= 1000),
    -- ⚠️ 暫時移除 ingredient_id（因為 INGREDIENT 表尚未建立）
    -- ingredient_id   bigint,
    is_active       boolean      NOT NULL DEFAULT true,
    created_at      timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT OPTION_pkey PRIMARY KEY (option_id),
    CONSTRAINT OPTION_o_category_id_fkey FOREIGN KEY (o_category_id)
        REFERENCES OPTION_CATEGORY(o_category_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    -- ⚠️ 暫時移除此外鍵約束
    -- CONSTRAINT OPTION_ingredient_id_fkey FOREIGN KEY (ingredient_id)
    --     REFERENCES INGREDIENT(ingredient_id)
    --     ON UPDATE CASCADE
    --     ON DELETE SET NULL
);

-- BRAND_PRODUCT_OPTION_RULE：商品在某選項群組的可選數量 & 預設選項
CREATE TABLE IF NOT EXISTS BRAND_PRODUCT_OPTION_RULE
(
    brand_id         bigint    NOT NULL,
    product_id       bigint    NOT NULL,
    o_category_id    bigint    NOT NULL,
    min_select       smallint  NOT NULL DEFAULT 0,
    max_select       smallint  NOT NULL DEFAULT 1,
    default_option_id bigint,
    updated_at       timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_pkey
        PRIMARY KEY (brand_id, product_id, o_category_id),
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_brand_id_fkey FOREIGN KEY (brand_id)
        REFERENCES BRAND(brand_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_product_id_fkey FOREIGN KEY (product_id)
        REFERENCES PRODUCT(product_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_o_category_id_fkey FOREIGN KEY (o_category_id)
        REFERENCES OPTION_CATEGORY(o_category_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_default_option_id_fkey FOREIGN KEY (default_option_id)
        REFERENCES OPTION(option_id)
        ON UPDATE SET NULL
        ON DELETE SET NULL,
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_min_select_chk CHECK (min_select >= 0),
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_max_select_chk CHECK (max_select >= min_select)
);

-- BRAND_PRODUCT_OPTION_MUTEX：選項互斥邏輯
CREATE TABLE IF NOT EXISTS BRAND_PRODUCT_OPTION_MUTEX
(
    mutex_id      bigserial   NOT NULL,
	brand_id      bigint      NOT NULL,
    product_id    bigint      NOT NULL,
    option_id_low bigint      NOT NULL,
    option_id_high bigint,
    mutex_logic   varchar(10) NOT NULL DEFAULT 'single'
        CHECK (
            (mutex_logic = 'single'    AND option_id_high IS NULL)
         OR (mutex_logic = 'exclusive' AND option_id_high IS NOT NULL)
        ),
     --' single'：單選互斥（option_id_high 為 NULL）
     --' exclusive'：互斥組合（option_id_high 不為 NULL）
    updated_at    timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_pkey
        PRIMARY KEY (mutex_id),
	CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_uniq
        UNIQUE (brand_id, product_id, option_id_low, option_id_high),
    CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_brand_id_fkey FOREIGN KEY (brand_id)
        REFERENCES BRAND(brand_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_product_id_fkey FOREIGN KEY (product_id)
        REFERENCES PRODUCT(product_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_option_id_low_fkey FOREIGN KEY (option_id_low)
        REFERENCES OPTION(option_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_option_id_high_fkey FOREIGN KEY (option_id_high)
        REFERENCES OPTION(option_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE    
);

-- STORE_OPTION：門市實際提供選項
CREATE TABLE IF NOT EXISTS STORE_OPTION
(
    store_id    bigint    NOT NULL,
    option_id   bigint    NOT NULL,
    is_enabled  boolean   NOT NULL DEFAULT true,
    updated_at  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT STORE_OPTION_pkey PRIMARY KEY (store_id, option_id),
    CONSTRAINT STORE_OPTION_store_id_fkey FOREIGN KEY (store_id)
        REFERENCES STORE(store_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT STORE_OPTION_option_id_fkey FOREIGN KEY (option_id)
        REFERENCES OPTION(option_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE

);
-- ============================
-- 以下暫時擱置（未來再實作）
-- ============================


-- -- INGREDIENT：原料
-- CREATE TABLE IF NOT EXISTS INGREDIENT
-- (
--     ingredient_id   bigserial NOT NULL,
--     brand_id        bigint    NOT NULL,
--     ingredient_name varchar(100) NOT NULL,
--     unit            varchar(10)  NOT NULL
--         CHECK (unit IN ('g', 'ml', 'piece')),
--     is_active       boolean   NOT NULL DEFAULT true,
--     created_at      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     updated_at      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT INGREDIENT_pkey PRIMARY KEY (ingredient_id),
--     CONSTRAINT INGREDIENT_brand_id_fkey FOREIGN KEY (brand_id)
--         REFERENCES BRAND(brand_id)
--         ON UPDATE CASCADE
--         ON DELETE CASCADE
-- );

-- -- PRODUCT_INGREDIENT：商品使用哪些原料、用量
-- CREATE TABLE IF NOT EXISTS PRODUCT_INGREDIENT
-- (
--     product_id     bigint NOT NULL,
--     ingredient_id  bigint NOT NULL,
--     qty            int    NOT NULL CHECK (qty >= 0),
--     updated_at     timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT PRODUCT_INGREDIENT_pkey PRIMARY KEY (product_id, ingredient_id),
--     CONSTRAINT PRODUCT_INGREDIENT_product_id_fkey FOREIGN KEY (product_id)
--         REFERENCES PRODUCT(product_id)
--         ON UPDATE CASCADE
--         ON DELETE CASCADE,
--     CONSTRAINT PRODUCT_INGREDIENT_ingredient_id_fkey FOREIGN KEY (ingredient_id)
--         REFERENCES INGREDIENT(ingredient_id)
--         ON UPDATE CASCADE
--         ON DELETE CASCADE
-- );

-- -- INVENTORY：各門市原料庫存
-- CREATE TABLE IF NOT EXISTS INVENTORY
-- (
--     store_id       bigint        NOT NULL,
--     ingredient_id  bigint        NOT NULL,
--     stock_level    int           NOT NULL CHECK (stock_level >= 0),
--     last_restock_at timestamp     NOT NULL,
--     updated_at     timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT INVENTORY_pkey PRIMARY KEY (store_id, ingredient_id),
--     CONSTRAINT INVENTORY_store_id_fkey FOREIGN KEY (store_id)
--         REFERENCES STORE(store_id)
--         ON UPDATE CASCADE
--         ON DELETE CASCADE,
--     CONSTRAINT INVENTORY_ingredient_id_fkey FOREIGN KEY (ingredient_id)
--         REFERENCES INGREDIENT(ingredient_id)
--         ON UPDATE CASCADE
--         ON DELETE CASCADE
-- );

