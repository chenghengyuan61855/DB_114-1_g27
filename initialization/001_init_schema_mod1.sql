CREATE TABLE IF NOT EXISTS BRAND
(
    brand_id bigserial NOT NULL,
    brand_name character varying(20) NOT NULL,
    brand_address character varying(100),
    brand_phone character varying(20),
    brand_email character varying(50),
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT BRAND_pkey PRIMARY KEY (brand_id),
    CONSTRAINT BRAND_brand_name_key UNIQUE (brand_name)
);

CREATE TABLE IF NOT EXISTS STORE
(
    store_id bigserial NOT NULL,
    brand_id bigint NOT NULL,
	store_name character varying(20) NOT NULL,
    store_address character varying(100),
    store_phone character varying(20),
    is_active boolean NOT NULL DEFAULT true,
	is_accepting_orders boolean NOT NULL DEFAULT true,
    created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	is_accepting_deliveries boolean NOT NULL DEFAULT true,
	min_order_total_price int,
    CONSTRAINT STORE_pkey PRIMARY KEY (store_id),
    CONSTRAINT STORE_brand_id_fkey FOREIGN KEY (brand_id)
        REFERENCES BRAND (brand_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS STORE_HOURS
(
    store_id bigint NOT NULL,
    weekday smallint NOT NULL
	    CHECK (weekday BETWEEN 0 AND 6),
    is_open boolean NOT NULL DEFAULT true,
    open_time time without time zone,
    close_time time without time zone,
    CONSTRAINT STORE_HOURS_pkey PRIMARY KEY (store_id, weekday),
    CONSTRAINT STORE_HOURS_store_id_fkey FOREIGN KEY (store_id)
        REFERENCES STORE (store_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS APP_USER
(
    user_id bigserial NOT NULL,
	user_name character varying(20) NOT NULL,
    user_phone character varying(20) NOT NULL,
    user_email character varying(50),
	password_hash varchar(100) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT USER_pkey PRIMARY KEY (user_id),
	CONSTRAINT USER_user_phone_key UNIQUE (user_phone),
	CONSTRAINT USER_user_email_key UNIQUE (user_email)
);

CREATE TABLE IF NOT EXISTS USER_ADDRESS
(
    user_id bigint NOT NULL,
	label character varying(20) NOT NULL,
    district character varying(50) NOT NULL,
	address varchar(100) NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT USER_ADDRESS_pkey PRIMARY KEY (user_id, label),
	CONSTRAINT USER_ADDRESS_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES APP_USER (user_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ROLE
(
    role_id serial NOT NULL,
	role_name character varying(20) NOT NULL,
    role_description character varying(200),
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ROLE_pkey PRIMARY KEY (role_id)
);

CREATE TABLE IF NOT EXISTS USER_ROLE_ASSIGNMENT
(
    user_role_id bigserial NOT NULL,
	user_id bigint NOT NULL,
	role_id int NOT NULL,
	scope_type character varying(10) NOT NULL
	    CHECK (scope_type IN ('global', 'brand', 'store')),
	brand_id bigint,
	store_id bigint,
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT USER_ROLE_ASSIGNMENT_pkey PRIMARY KEY (user_role_id),
	CONSTRAINT USER_ROLE_ASSIGNMENT_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES APP_USER (user_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
	CONSTRAINT USER_ROLE_ASSIGNMENT_role_id_fkey FOREIGN KEY (role_id)
        REFERENCES ROLE (role_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
	CONSTRAINT USER_ROLE_ASSIGNMENT_brand_id_fkey FOREIGN KEY (brand_id)
        REFERENCES BRAND (brand_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
	CONSTRAINT USER_ROLE_ASSIGNMENT_store_id_fkey FOREIGN KEY (store_id)
        REFERENCES STORE (store_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
	CHECK (
	    (scope_type = 'global' AND brand_id IS NULL AND store_id IS NULL)
		OR
        (scope_type = 'brand' AND brand_id IS NOT NULL AND store_id IS NULL)
        OR
        (scope_type = 'store' AND store_id IS NOT NULL AND brand_id IS NULL)
    )

);
