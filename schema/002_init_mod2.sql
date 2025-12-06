-- PRODUCT_CATEGORY：商品類別
CREATE TABLE IF NOT EXISTS PRODUCT_CATEGORY
(
    p_category_id        bigserial      NOT NULL,
    brand_id             bigint         NOT NULL,
    p_category_name      text           NOT NULL,
    p_category_description varchar(100),
    display_order        int,
    is_active            boolean        NOT NULL DEFAULT true,
    created_at           timestamp      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at           timestamp      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PRODUCT_CATEGORY_pkey PRIMARY KEY (p_category_id),
    CONSTRAINT PRODUCT_CATEGORY_brand_id_fkey FOREIGN KEY (brand_id)
        REFERENCES BRAND(brand_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT PRODUCT_CATEGORY_display_order_chk
        CHECK (display_order IS NULL OR display_order >= 0)
);

-- PRODUCT：商品
CREATE TABLE IF NOT EXISTS PRODUCT
(
    product_id           bigserial      NOT NULL,
    brand_id             bigint         NOT NULL,
    p_category_id        bigint,
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
        ON DELETE CASCADE,
    CONSTRAINT PRODUCT_p_category_id_fkey FOREIGN KEY (p_category_id)
        REFERENCES PRODUCT_CATEGORY(p_category_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
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

-- INGREDIENT：原料
CREATE TABLE IF NOT EXISTS INGREDIENT
(
    ingredient_id   bigserial NOT NULL,
    brand_id        bigint    NOT NULL,
    ingredient_name varchar(100) NOT NULL,
    unit            varchar(10)  NOT NULL
        CHECK (unit IN ('g', 'ml', 'piece')),
    is_active       boolean   NOT NULL DEFAULT true,
    created_at      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT INGREDIENT_pkey PRIMARY KEY (ingredient_id),
    CONSTRAINT INGREDIENT_brand_id_fkey FOREIGN KEY (brand_id)
        REFERENCES BRAND(brand_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- PRODUCT_INGREDIENT：商品使用哪些原料、用量
CREATE TABLE IF NOT EXISTS PRODUCT_INGREDIENT
(
    product_id     bigint NOT NULL,
    ingredient_id  bigint NOT NULL,
    qty            int    NOT NULL CHECK (qty >= 0),
    updated_at     timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PRODUCT_INGREDIENT_pkey PRIMARY KEY (product_id, ingredient_id),
    CONSTRAINT PRODUCT_INGREDIENT_product_id_fkey FOREIGN KEY (product_id)
        REFERENCES PRODUCT(product_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT PRODUCT_INGREDIENT_ingredient_id_fkey FOREIGN KEY (ingredient_id)
        REFERENCES INGREDIENT(ingredient_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- INVENTORY：各門市原料庫存
CREATE TABLE IF NOT EXISTS INVENTORY
(
    store_id       bigint        NOT NULL,
    ingredient_id  bigint        NOT NULL,
    stock_level    int           NOT NULL CHECK (stock_level >= 0),
    last_restock_at timestamp     NOT NULL,
    updated_at     timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT INVENTORY_pkey PRIMARY KEY (store_id, ingredient_id),
    CONSTRAINT INVENTORY_store_id_fkey FOREIGN KEY (store_id)
        REFERENCES STORE(store_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT INVENTORY_ingredient_id_fkey FOREIGN KEY (ingredient_id)
        REFERENCES INGREDIENT(ingredient_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
