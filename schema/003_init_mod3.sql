-- OPTION_CATEGORY：選項群組
CREATE TABLE IF NOT EXISTS public."OPTION_CATEGORY"
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
        REFERENCES public."BRAND"(brand_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT OPTION_CATEGORY_display_order_chk
        CHECK (display_order IS NULL OR display_order >= 0)
);

-- OPTION：單一選項（加料／甜度冰塊等）
CREATE TABLE IF NOT EXISTS public."OPTION"
(
    option_id      bigserial     NOT NULL,
    o_category_id  bigint        NOT NULL,
    option_name    varchar(100)  NOT NULL,
    price_adjust   int           NOT NULL,
    ingredient_id  bigint,
    usage_qty      int,
    is_active      boolean       NOT NULL DEFAULT true,
    created_at     timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT OPTION_pkey PRIMARY KEY (option_id),
    CONSTRAINT OPTION_o_category_id_fkey FOREIGN KEY (o_category_id)
        REFERENCES public."OPTION_CATEGORY"(o_category_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT OPTION_ingredient_id_fkey FOREIGN KEY (ingredient_id)
        REFERENCES public."INGREDIENT"(ingredient_id)
        ON UPDATE SET NULL
        ON DELETE SET NULL,
    CONSTRAINT OPTION_usage_qty_chk CHECK (usage_qty IS NULL OR usage_qty >= 0)
);

-- BRAND_PRODUCT_OPTION_RULE：商品在某選項群組的可選數量 & 預設選項
CREATE TABLE IF NOT EXISTS public."BRAND_PRODUCT_OPTION_RULE"
(
    brand_id         bigint    NOT NULL,
    product_id       bigint    NOT NULL,
    o_category_id    bigint    NOT NULL,
    min_select       smallint  NOT NULL,
    max_select       smallint  NOT NULL,
    default_option_id bigint,
    updated_at       timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_pkey
        PRIMARY KEY (brand_id, product_id, o_category_id),
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_brand_id_fkey FOREIGN KEY (brand_id)
        REFERENCES public."BRAND"(brand_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_product_id_fkey FOREIGN KEY (product_id)
        REFERENCES public."PRODUCT"(product_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_o_category_id_fkey FOREIGN KEY (o_category_id)
        REFERENCES public."OPTION_CATEGORY"(o_category_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_default_option_id_fkey FOREIGN KEY (default_option_id)
        REFERENCES public."OPTION"(option_id)
        ON UPDATE SET NULL
        ON DELETE SET NULL,
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_min_select_chk CHECK (min_select >= 0),
    CONSTRAINT BRAND_PRODUCT_OPTION_RULE_max_select_chk CHECK (max_select >= min_select)
);

-- BRAND_PRODUCT_OPTION_MUTEX：選項互斥邏輯
CREATE TABLE IF NOT EXISTS public."BRAND_PRODUCT_OPTION_MUTEX"
(
    mutex_id      bigserial   NOT NULL,
	brand_id      bigint      NOT NULL,
    product_id    bigint      NOT NULL,
    option_id_low bigint      NOT NULL,
    option_id_high bigint,
    mutex_logic   varchar(10) NOT NULL,
    updated_at    timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_pkey
        PRIMARY KEY (mutex_id),
	CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_uniq
        UNIQUE (brand_id, product_id, option_id_low, option_id_high),
    CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_brand_id_fkey FOREIGN KEY (brand_id)
        REFERENCES public."BRAND"(brand_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_product_id_fkey FOREIGN KEY (product_id)
        REFERENCES public."PRODUCT"(product_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_option_id_low_fkey FOREIGN KEY (option_id_low)
        REFERENCES public."OPTION"(option_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_option_id_high_fkey FOREIGN KEY (option_id_high)
        REFERENCES public."OPTION"(option_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT BRAND_PRODUCT_OPTION_MUTEX_logic_chk
        CHECK (
            (mutex_logic = 'single'    AND option_id_high IS NULL)
         OR (mutex_logic = 'exclusive' AND option_id_high IS NOT NULL)
        )
);

-- STORE_OPTION：門市實際提供選項
CREATE TABLE IF NOT EXISTS public."STORE_OPTION"
(
    store_id    bigint    NOT NULL,
    option_id   bigint    NOT NULL,
    is_enabled  boolean   NOT NULL DEFAULT true,
    updated_at  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT STORE_OPTION_pkey PRIMARY KEY (store_id, option_id),
    CONSTRAINT STORE_OPTION_store_id_fkey FOREIGN KEY (store_id)
        REFERENCES public."STORE"(store_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT STORE_OPTION_option_id_fkey FOREIGN KEY (option_id)
        REFERENCES public."OPTION"(option_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);