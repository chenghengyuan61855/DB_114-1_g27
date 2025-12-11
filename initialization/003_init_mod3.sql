-- ORDERS：訂單主檔
CREATE TABLE IF NOT EXISTS ORDERS
(
    order_id        bigserial     NOT NULL,
    user_id         bigint        NOT NULL,
    store_id        bigint        NOT NULL,
    order_status    varchar(10)   NOT NULL DEFAULT 'placed',
    order_type      varchar(10)   NOT NULL DEFAULT 'pickup',
    delivery_address varchar(100),
    receiver_name   varchar(20),
    receiver_phone  varchar(20),
    placed_at       timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    accepted_at     timestamp,
    completed_at    timestamp,
    rejected_reason varchar(50),
    total_price     int           NOT NULL DEFAULT 0,
    payment_status  varchar(10)   NOT NULL DEFAULT 'unpaid',
    payment_method  varchar(10)   NOT NULL DEFAULT 'cash',
    CONSTRAINT ORDERS_pkey PRIMARY KEY (order_id),
    CONSTRAINT ORDERS_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES APP_USER(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT ORDERS_store_id_fkey FOREIGN KEY (store_id)
        REFERENCES STORE(store_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    -- 狀態／型別／付款相關的 domain
    CONSTRAINT ORDERS_status_chk CHECK (
        order_status IN ('placed', 'accepted', 'rejected', 'completed', 'cancelled')
    ),
    CONSTRAINT ORDERS_type_chk CHECK (
        order_type IN ('pickup', 'delivery')
    ),
    CONSTRAINT ORDERS_payment_status_chk CHECK (
        payment_status IN ('unpaid', 'paid', 'refunded')
    ),
    CONSTRAINT ORDERS_payment_method_chk CHECK (
        payment_method IN ('cash', 'card', 'online')
    ),
    CONSTRAINT ORDERS_total_price_chk CHECK (total_price >= 0)
);

-- ORDER_ITEM：訂單明細
CREATE TABLE IF NOT EXISTS ORDER_ITEM
(
    order_item_id      bigserial   NOT NULL,
    order_id           bigint      NOT NULL,
    product_id         bigint      NOT NULL,
    unit_price         int         NOT NULL DEFAULT 0,
    qty                smallint    NOT NULL DEFAULT 1,
    option_total_adjust int        NOT NULL DEFAULT 0,
    line_total_price   int         NOT NULL DEFAULT 0,
    CONSTRAINT ORDER_ITEM_pkey PRIMARY KEY (order_item_id),
    CONSTRAINT ORDER_ITEM_order_id_fkey FOREIGN KEY (order_id)
        REFERENCES ORDERS(order_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT ORDER_ITEM_product_id_fkey FOREIGN KEY (product_id)
        REFERENCES PRODUCT(product_id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT ORDER_ITEM_unit_price_chk CHECK (unit_price >= 0),
    CONSTRAINT ORDER_ITEM_qty_chk CHECK (qty > 0),
    CONSTRAINT ORDER_ITEM_line_total_chk CHECK (line_total_price >= 0)
);

-- ORDER_ITEM_OPTION：明細的實際選項（加料／甜度等）
CREATE TABLE IF NOT EXISTS ORDER_ITEM_OPTION
(
    order_item_id  bigint NOT NULL,
    option_id      bigint NOT NULL,
    CONSTRAINT ORDER_ITEM_OPTION_pkey PRIMARY KEY (order_item_id, option_id),
    CONSTRAINT ORDER_ITEM_OPTION_order_item_id_fkey FOREIGN KEY (order_item_id)
        REFERENCES ORDER_ITEM(order_item_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT ORDER_ITEM_OPTION_option_id_fkey FOREIGN KEY (option_id)
        REFERENCES OPTION(option_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- ORDER_RATING：整張訂單的評分
CREATE TABLE IF NOT EXISTS ORDER_RATING
(
    order_id       bigint      NOT NULL,
    order_rating   smallint    NOT NULL,
    order_comment  varchar(200),
    created_at     timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ORDER_RATING_pkey PRIMARY KEY (order_id),
    CONSTRAINT ORDER_RATING_order_id_fkey FOREIGN KEY (order_id)
        REFERENCES ORDERS(order_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT ORDER_RATING_rating_chk CHECK (order_rating BETWEEN 1 AND 5)
);

-- ORDER_ITEM_RATING：單一品項的評分
CREATE TABLE IF NOT EXISTS ORDER_ITEM_RATING
(
    order_item_id      bigint      NOT NULL,
    order_item_rating  smallint    NOT NULL,
    order_item_comment varchar(200),
    created_at         timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ORDER_ITEM_RATING_pkey PRIMARY KEY (order_item_id),
    CONSTRAINT ORDER_ITEM_RATING_order_item_id_fkey FOREIGN KEY (order_item_id)
        REFERENCES ORDER_ITEM(order_item_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT ORDER_ITEM_RATING_rating_chk CHECK (order_item_rating BETWEEN 1 AND 5)
);


