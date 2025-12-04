ALLOWED_TABLES = {
    # ===== User / ROLE =====
    "APP_USER", "USER_ADDRESS", "ROLE", "USER_ROLE_ASSIGNMENT",

    # ===== Brand / Store =====
    "BRAND", "STORE", "STORE_HOURS",
    
    # ===== Product =====
    "PRODUCT_CATEGORY", "PRODUCT", "STORE_PRODUCT",

    # ===== Ingredient / Inventory =====
    "INGREDIENT", "PRODUCT_INGREDIENT", "INVENTORY",

    # ===== Option / Customization =====
    "OPTION_CATEGORY", "OPTION", "BRAND_PRODUCT_OPTION_RULE",
    "BRAND_PRODUCT_OPTION_MUTEX", "STORE_OPTION",

    # ===== Order =====
    "ORDERS", "ORDER_ITEM", "ORDER_ITEM_OPTION",
    "ORDER_RATING", "ORDER_ITEM_RATING"
}

ALLOWED_COLUMNS = {
    # ================== User / Auth ==================
    "APP_USER": {"user_id","user_name","user_phone","user_email",
                 "password_hash","is_active", "created_at","updated_at"
    },

    "USER_ADDRESS": {"user_id","label","district","address",
                     "created_at","updated_at"
    },

    "ROLE": {"role_id","role_name","role_description",
             "password_hash","is_active","created_at","updated_at"
    },

    "USER_ROLE_ASSIGNMENT": {"user_role_id", "user_id","role_id","scope_type",
                             "brand_id","store_id","is_active","created_at","updated_at"
    },

    # ================== Brand / Store ==================
    "BRAND": {"brand_id","brand_name","brand_address","brand_phone",
              "brand_email","is_active", "created_at", "updated_at"
    },

    "STORE": {"store_id","brand_id","store_name","store_address","store_phone",
              "is_active","is_accepting_orders","is_accepting_deliveries",
              "min_order_qty","min_order_total_price","delivery_threshold_logic",
              "created_at","updated_at"
    },

    "STORE_HOURS": {"store_id","weekday","is_open","open_time","close_time"},

    # ================== Product ==================
    "PRODUCT_CATEGORY": {"p_category_id","brand_id","p_category_name",
                         "p_category_description","display_order",
                         "is_active","created_at","updated_at"
    },

    "PRODUCT": {"product_id","brand_id","p_category_id","product_name",
                "size","product_description","image_url",
                "is_active","created_at","updated_at"
    },

    "STORE_PRODUCT": {"store_id","product_id","price",
                      "is_active","created_at","updated_at"
    },

    # ================== Ingredient / Inventory ==================
    "INGREDIENT": {"ingredient_id","brand_id","ingredient_name",
                   "unit","is_active","created_at","updated_at"
    },

    "PRODUCT_INGREDIENT": {"product_id","ingredient_id","qty","updated_at"},

    "INVENTORY": {"store_id","ingredient_id","stock_level",
                  "last_restock_at","updated_at"
    },

    # ================== Option / Customization ==================
    "OPTION_CATEGORY": {"o_category_id","brand_id","o_category_name",
                        "display_order","is_active","created_at","updated_at"
    },

    "OPTION": {"option_id","o_category_id","option_name","price_adjust",
               "ingredient_id","usage_qty","is_active","created_at","updated_at"
    },

    "BRAND_PRODUCT_OPTION_RULE": {"brand_id","product_id","o_category_id",
                                  "min_select","max_select",
                                  "default_option_id","updated_at"
    },

    "BRAND_PRODUCT_OPTION_MUTEX": {"mutex_id","brand_id","product_id",
                                   "option_id_low","option_id_high",
                                   "mutex_logic","updated_at"
    },

    "STORE_OPTION": {"store_id","option_id","is_enabled","updated_at",},

    # ================== Order / Rating ==================
    "ORDERS": {"order_id","user_id","store_id","order_status","order_type",
               "placed_at","accepted_at","completed_at","cancelled_at",
               "total_price","payment_status","payment_method",
               "created_at","updated_at"
    },

    "ORDER_ITEM": {"order_item_id","order_id","product_id","unit_price","qty",
                   "option_total_adjust","line_total_price",
                   "created_at","updated_at"
    },

    "ORDER_ITEM_OPTION": {"order_item_id","option_id",
                          "price_adjust","created_at","updated_at"
    },

    "ORDER_RATING": {"rating_id","order_id","rating",
                     "comment","created_at","updated_at"
    },

    "ORDER_ITEM_RATING": {"item_rating_id","order_item_id",
                          "rating","comment","created_at","updated_at",
    },
}
