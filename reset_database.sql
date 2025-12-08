-- =============================================
-- 完整重建資料庫
-- =============================================

-- 1. 清空所有表（保留結構）
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE';
    END LOOP;
END $$;

-- =============================================
-- 2. 插入基礎資料
-- =============================================

-- 角色
INSERT INTO ROLE (role_name, role_description) VALUES 
('member', '一般消費者，可跨店點餐'),
('store_staff', '門市人員，管理特定門市訂單'),
('brand_manager', '品牌管理者，管理商品與菜單');

-- 品牌
INSERT INTO BRAND (brand_name, brand_address, brand_phone, brand_email, is_active) VALUES 
-- 1. 可不可熟成紅茶 (資料來源：永醇誠股份有限公司)
('可不可熟成紅茶', '臺中市北屯區文心路四段448號', '0800-000-961', NULL, true),
-- 2. 50嵐 (資料來源：深耕茶業股份有限公司 - 北區總部)
('50嵐', '臺北市中正區忠孝西路1段100號', '0800-600-150', 'service@50lan.com', true),
-- 3. 得正 (資料來源：永得正文化有限公司)
('得正', '臺中市北屯區后庄里松竹路三段726號', '04-24258800', NULL, true),
-- 4. 麻古茶坊 (資料來源：麻古茶坊總部)
('麻古茶坊', '高雄市左營區文育路72號', '07-3450111', NULL, true),
-- 5. 迷客夏 (資料來源：迷客夏國際股份有限公司)
('迷客夏', '台南市北區西門路四段271號7樓之8', '06-2818569', NULL, true);

-- 門市
INSERT INTO STORE (brand_id, store_name, store_address, store_phone, is_active, is_accepting_orders, is_accepting_deliveries) VALUES 
(1, '台北公館店', '台北市中正區汀州路三段174號', '02-23680270', true, true, true),          -- 可不可熟成紅茶
(2, '50嵐_公館店', '10091臺北市中正區汀州路三段116-1號', '02-23684599', true, true, true),        -- 50嵐 (老字號台大店)
(2, '50嵐_復興店', '10664臺北市大安區復興南路二段182號', '02-27093698', true, true, true),         -- 50嵐 復興店
(2, '50嵐_永康店', '10650臺北市大安區永康街14巷2號', '02-23952000', true, true, true),             -- 50嵐 永康店
(2, '50嵐_同安店', '100臺北市中正區同安街32號', '02-23653381', true, true, true),                   -- 50嵐 同安店
(2, '50嵐_通化店', '10678臺北市大安區通化街119號', '02-27399748', true, true, true),               -- 50嵐 通化店
(3, '台北公館計劃', '台北市中正區羅斯福路三段316巷10-2號', '02-23683130', true, true, true), -- 得正 (特色店名)
(4, '台北公館店', '100臺北市中正區羅斯福路三段316巷5號', '02-23672307', true, true, true),      -- 麻古茶坊
(5, '台北公館店', '10090臺北市中正區羅斯福路三段316巷10之2號1樓', '02-23687707', true, true, true);         -- 迷客夏


-- =============================================
-- 3. 商品
-- =============================================

-- 可不可 (product_id 1~10)
INSERT INTO PRODUCT (brand_id, product_name, product_description, is_active) VALUES 
(1, '熟成紅茶', '解油膩，帶有果香的經典紅茶', true),
(1, '麗春紅茶', '帶有花香的斯里蘭卡紅茶', true),
(1, '太妃紅茶', '咖啡與紅茶的神秘比例', true),
(1, '胭脂紅茶', '帶有蜜桃風味的果香紅茶', true),
(1, '春芽綠茶', '清爽甘甜的綠茶', true),
(1, '熟成歐蕾', '熟成紅茶與鮮奶的完美比例', true),
(1, '白玉歐蕾', '熟成歐蕾加上Q彈白玉珍珠', true),
(1, '冷露歐蕾', '手工冬瓜露搭配鮮奶', true),
(1, '春芽冷露', '綠茶混冬瓜茶', true),
(1, '胭脂多多', '蜜桃紅茶加養樂多', true);

-- 50嵐 (product_id 11~20)
INSERT INTO PRODUCT (brand_id, product_name, product_description, is_active) VALUES 
(2, '四季春青茶', '順口回甘，經典好茶', true),
(2, '黃金烏龍', '香氣濃郁的烏龍茶', true),
(2, '8冰綠', '金桔汁與梅汁搭配綠茶', true),
(2, '冰淇淋紅茶', '香草冰淇淋加上紅茶', true),
(2, '波霸奶茶', '大顆珍珠搭配奶茶', true),
(2, '珍珠奶茶', '小顆珍珠搭配奶茶', true),
(2, '四季春珍波椰', '四季春加珍珠波霸椰果，超滿足', true),
(2, '燕麥奶茶', '健康燕麥搭配奶茶', true),
(2, '阿薩姆紅茶', '經典紅茶', true),
(2, '旺來紅', '鳳梨果醬搭配紅茶', true);

-- 得正 (product_id 21~30)
INSERT INTO PRODUCT (brand_id, product_name, product_description, is_active) VALUES 
(3, '春烏龍', '輕發酵，口感清爽', true),
(3, '輕烏龍', '中發酵，茶味適中', true),
(3, '焙烏龍', '重烘焙，香氣濃郁', true),
(3, '檸檬春烏龍', '新鮮檸檬搭配春烏龍', true),
(3, '芝士奶蓋春烏龍', '鹹甜奶蓋搭配清爽烏龍', true),
(3, '焙烏龍奶茶', '濃厚茶香奶茶', true),
(3, '焙烏龍鮮奶', '鮮奶搭配重焙烏龍', true),
(3, '優酪春烏龍', '乳酸飲搭配烏龍茶', true),
(3, '甘蔗春烏龍', '甘蔗原汁搭配烏龍', true),
(3, '黃金珍珠奶綠', '奶綠搭配黃金珍珠', true);

-- 麻古 (product_id 31~40)
INSERT INTO PRODUCT (brand_id, product_name, product_description, is_active) VALUES 
(4, '高山金萱茶', '淡雅奶香的金萱茶', true),
(4, '翡翠綠茶', '清爽綠茶', true),
(4, '楊枝甘露2.0', '芒果冰沙、葡萄柚、椰奶、茶凍', true),
(4, '芝芝葡萄果粒', '巨峰葡萄冰沙加奶蓋', true),
(4, '柳橙果粒茶', '滿滿柳橙果肉', true),
(4, '番茄梅蜜', '小番茄打成冰沙加梅汁', true),
(4, '芋泥波波鮮奶', '大甲芋頭加珍珠鮮奶', true),
(4, '波霸紅茶拿鐵', '鮮奶茶加波霸', true),
(4, '香橙果粒茶', '柳橙切片加綠茶', true),
(4, '金萱雙Q', '金萱茶加珍珠與椰果', true);

-- 迷客夏 (product_id 41~50)
INSERT INTO PRODUCT (brand_id, product_name, product_description, is_active) VALUES 
(5, '大正紅茶拿鐵', '古早味紅茶加鮮奶', true),
(5, '伯爵紅茶拿鐵', '佛手柑香氣紅茶加鮮奶', true),
(5, '珍珠紅茶拿鐵', '白玉珍珠鮮奶茶', true),
(5, '芋頭鮮奶', '手搗芋泥加鮮奶', true),
(5, '手炒黑糖鮮奶', '黑糖鮮奶', true),
(5, '原片初露青茶', '台灣青茶', true),
(5, '琥珀高峰烏龍', '炭焙香氣烏龍', true),
(5, '決明大麥', '自帶甜味的大麥茶', true),
(5, '青檸香茶', '手搖檸檬皮香氣', true),
(5, '柳丁綠茶', '台灣柳丁汁加綠茶', true);

-- =============================================
-- 4. 門市商品定價
-- =============================================

-- 可不可
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(1, 1, 35, true), (1, 2, 35, true), (1, 3, 40, true), (1, 4, 45, true), (1, 5, 35, true),
(1, 6, 50, true), (1, 7, 60, true), (1, 8, 50, true), (1, 9, 45, true), (1, 10, 50, true);

-- 50嵐_公館店
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(2, 11, 30, true), (2, 12, 40, true), (2, 13, 50, true), (2, 14, 50, true), (2, 15, 55, true),
(2, 16, 50, true), (2, 17, 45, true), (2, 18, 60, true), (2, 19, 30, true), (2, 20, 55, true);

-- 50嵐_復興店
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(3, 11, 30, true), (3, 12, 40, true), (3, 13, 50, true), (3, 14, 50, true), (3, 15, 55, true),
(3, 16, 50, true), (3, 17, 45, true), (3, 18, 60, true), (3, 19, 30, true), (3, 20, 55, true);

-- 50嵐_永康店
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(4, 11, 30, true), (4, 12, 40, true), (4, 13, 50, true), (4, 14, 50, true), (4, 15, 55, true),
(4, 16, 50, true), (4, 17, 45, true), (4, 18, 60, true), (4, 19, 30, true), (4, 20, 55, true);

-- 50嵐_同安店
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(5, 11, 30, true), (5, 12, 40, true), (5, 13, 50, true), (5, 14, 50, true), (5, 15, 55, true),
(5, 16, 50, true), (5, 17, 45, true), (5, 18, 60, true), (5, 19, 30, true), (5, 20, 55, true);

-- 50嵐_通化店
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(6, 11, 30, true), (6, 12, 40, true), (6, 13, 50, true), (6, 14, 50, true), (6, 15, 55, true),
(6, 16, 50, true), (6, 17, 45, true), (6, 18, 60, true), (6, 19, 30, true), (6, 20, 55, true);

-- 得正
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(7, 21, 35, true), (7, 22, 35, true), (7, 23, 35, true), (7, 24, 55, true), (7, 25, 60, true),
(7, 26, 50, true), (7, 27, 60, true), (7, 28, 55, true), (7, 29, 55, true), (7, 30, 55, true);

-- 麻古
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(8, 31, 35, true), (8, 32, 35, true), (8, 33, 80, true), (8, 34, 90, true), (8, 35, 75, true),
(8, 36, 70, true), (8, 37, 85, true), (8, 38, 60, true), (8, 39, 75, true), (8, 40, 50, true);

-- 迷客夏
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(9, 41, 55, true), (9, 42, 60, true), (9, 43, 65, true), (9, 44, 70, true), (9, 45, 65, true),
(9, 46, 35, true), (9, 47, 40, true), (9, 48, 35, true), (9, 49, 60, true), (9, 50, 45, true);


-- =============================================
-- 5. 選項分類
-- =============================================

INSERT INTO OPTION_CATEGORY (brand_id, o_category_name, display_order, is_active) VALUES 
-- 可不可 (1)
(1, '甜度', 1, true),
(1, '冰塊', 2, true),
(1, '加料', 3, true),
-- 50嵐 (2)
(2, '甜度', 1, true),
(2, '冰塊', 2, true),
(2, '加料', 3, true),
-- 得正 (3)
(3, '甜度', 1, true),
(3, '冰塊', 2, true),
(3, '加料', 3, true),
-- 麻古茶坊 (4)
(4, '甜度', 1, true),
(4, '冰塊', 2, true),
(4, '加料', 3, true),
-- 迷客夏 (5)
(5, '甜度', 1, true),
(5, '冰塊', 2, true),
(5, '加料', 3, true);

-- =============================================
-- 6. 選項
-- =============================================

INSERT INTO OPTION (o_category_id, option_name, price_adjust, is_active) VALUES 
-- 甜度 (0元)
(1, '正常糖', 0, true),(1, '半糖', 0, true),(1, '微糖', 0, true),(1, '無糖', 0, true),
(4, '正常糖', 0, true),(4, '半糖', 0, true),(4, '微糖', 0, true),(4, '無糖', 0, true),
(7, '正常糖', 0, true),(7, '半糖', 0, true),(7, '微糖', 0, true),(7, '無糖', 0, true),
(10, '正常糖', 0, true),(10, '半糖', 0, true),(10, '微糖', 0, true),(10, '無糖', 0, true),
(13, '正常糖', 0, true),(13, '半糖', 0, true),(13, '微糖', 0, true),(13, '無糖', 0, true),

-- 冰塊 (0元)
(2, '正常冰', 0, true),(2, '少冰', 0, true),(2, '去冰', 0, true),(2, '熱', 0, true),
(5, '正常冰', 0, true),(5, '少冰', 0, true),(5, '去冰', 0, true),(5, '熱', 0, true),
(8, '正常冰', 0, true),(8, '少冰', 0, true),(8, '去冰', 0, true),(8, '熱', 0, true),
(11, '正常冰', 0, true),(11, '少冰', 0, true),(11, '去冰', 0, true),(11, '熱', 0, true),
(14, '正常冰', 0, true),(14, '少冰', 0, true),(14, '去冰', 0, true),(14, '熱', 0, true),

-- 加料 (價格依品牌常見)
(3, '加白玉珍珠', 10, true),(3, '加水玉', 10, true),(3, '加珍珠波霸', 10, true),(3, '加椰果', 10, true),(3, '加燕麥', 15, true),
(6, '加珍珠波霸', 10, true),(6, '加椰果', 10, true),(6, '加冰淇淋', 20, true),(6, '加奶蓋', 15, true),
(9, '加芝士奶蓋', 15, true),(9, '加黃金珍珠', 10, true),(9, '加甘蔗', 10, true),
(12, '加奶蓋', 15, true),(12, '加珍珠', 10, true),(12, '加椰果', 10, true),(12, '加果粒', 10, true),
(15, '加珍珠', 10, true),(15, '加芋頭', 15, true),(15, '加黑糖', 10, true);

-- =============================================
-- 7. 商品選項規則（關鍵！修正 product_id 範圍）
-- =============================================

-- 可不可 (product_id 1~10, o_category_id 1,2,3)
INSERT INTO BRAND_PRODUCT_OPTION_RULE (brand_id, product_id, o_category_id, min_select, max_select) VALUES
(1,1,1,1,1),(1,1,2,1,1),(1,1,3,0,2),
(1,2,1,1,1),(1,2,2,1,1),(1,2,3,0,2),
(1,3,1,1,1),(1,3,2,1,1),(1,3,3,0,2),
(1,4,1,1,1),(1,4,2,1,1),(1,4,3,0,2),
(1,5,1,1,1),(1,5,2,1,1),(1,5,3,0,2),
(1,6,1,1,1),(1,6,2,1,1),(1,6,3,0,2),
(1,7,1,1,1),(1,7,2,1,1),(1,7,3,0,2),
(1,8,1,1,1),(1,8,2,1,1),(1,8,3,0,2),
(1,9,1,1,1),(1,9,2,1,1),(1,9,3,0,2),
(1,10,1,1,1),(1,10,2,1,1),(1,10,3,0,2);

-- 50嵐 (product_id 11~20, o_category_id 4,5,6) ← ✅ 修正！
INSERT INTO BRAND_PRODUCT_OPTION_RULE (brand_id, product_id, o_category_id, min_select, max_select) VALUES
(2,11,4,1,1),(2,11,5,1,1),(2,11,6,0,2),
(2,12,4,1,1),(2,12,5,1,1),(2,12,6,0,2),
(2,13,4,1,1),(2,13,5,1,1),(2,13,6,0,2),
(2,14,4,1,1),(2,14,5,1,1),(2,14,6,0,2),
(2,15,4,1,1),(2,15,5,1,1),(2,15,6,0,2),
(2,16,4,1,1),(2,16,5,1,1),(2,16,6,0,2),
(2,17,4,1,1),(2,17,5,1,1),(2,17,6,0,2),
(2,18,4,1,1),(2,18,5,1,1),(2,18,6,0,2),
(2,19,4,1,1),(2,19,5,1,1),(2,19,6,0,2),
(2,20,4,1,1),(2,20,5,1,1),(2,20,6,0,2);

-- 得正 (product_id 21~30, o_category_id 7,8,9)
INSERT INTO BRAND_PRODUCT_OPTION_RULE (brand_id, product_id, o_category_id, min_select, max_select) VALUES
(3,21,7,1,1),(3,21,8,1,1),(3,21,9,0,2),
(3,22,7,1,1),(3,22,8,1,1),(3,22,9,0,2),
(3,23,7,1,1),(3,23,8,1,1),(3,23,9,0,2),
(3,24,7,1,1),(3,24,8,1,1),(3,24,9,0,2),
(3,25,7,1,1),(3,25,8,1,1),(3,25,9,0,2),
(3,26,7,1,1),(3,26,8,1,1),(3,26,9,0,2),
(3,27,7,1,1),(3,27,8,1,1),(3,27,9,0,2),
(3,28,7,1,1),(3,28,8,1,1),(3,28,9,0,2),
(3,29,7,1,1),(3,29,8,1,1),(3,29,9,0,2),
(3,30,7,1,1),(3,30,8,1,1),(3,30,9,0,2);

-- 麻古茶坊 (product_id 31~40, o_category_id 10,11,12)
INSERT INTO BRAND_PRODUCT_OPTION_RULE (brand_id, product_id, o_category_id, min_select, max_select) VALUES
(4,31,10,1,1),(4,31,11,1,1),(4,31,12,0,2),
(4,32,10,1,1),(4,32,11,1,1),(4,32,12,0,2),
(4,33,10,1,1),(4,33,11,1,1),(4,33,12,0,2),
(4,34,10,1,1),(4,34,11,1,1),(4,34,12,0,2),
(4,35,10,1,1),(4,35,11,1,1),(4,35,12,0,2),
(4,36,10,1,1),(4,36,11,1,1),(4,36,12,0,2),
(4,37,10,1,1),(4,37,11,1,1),(4,37,12,0,2),
(4,38,10,1,1),(4,38,11,1,1),(4,38,12,0,2),
(4,39,10,1,1),(4,39,11,1,1),(4,39,12,0,2),
(4,40,10,1,1),(4,40,11,1,1),(4,40,12,0,2);

-- 迷客夏 (product_id 41~50, o_category_id 13,14,15)
INSERT INTO BRAND_PRODUCT_OPTION_RULE (brand_id, product_id, o_category_id, min_select, max_select) VALUES
(5,41,13,1,1),(5,41,14,1,1),(5,41,15,0,2),
(5,42,13,1,1),(5,42,14,1,1),(5,42,15,0,2),
(5,43,13,1,1),(5,43,14,1,1),(5,43,15,0,2),
(5,44,13,1,1),(5,44,14,1,1),(5,44,15,0,2),
(5,45,13,1,1),(5,45,14,1,1),(5,45,15,0,2),
(5,46,13,1,1),(5,46,14,1,1),(5,46,15,0,2),
(5,47,13,1,1),(5,47,14,1,1),(5,47,15,0,2),
(5,48,13,1,1),(5,48,14,1,1),(5,48,15,0,2),
(5,49,13,1,1),(5,49,14,1,1),(5,49,15,0,2),
(5,50,13,1,1),(5,50,14,1,1),(5,50,15,0,2);

-- =============================================
-- 8. 門市選項啟用
-- =============================================

-- ✅ 修正：門市只擁有自己品牌的選項
INSERT INTO STORE_OPTION (store_id, option_id, is_enabled)
SELECT s.store_id, o.option_id, true
FROM STORE s
INNER JOIN OPTION o ON o.o_category_id IN (
    SELECT oc.o_category_id
    FROM OPTION_CATEGORY oc
    WHERE oc.brand_id = s.brand_id
)
WHERE s.is_active = true 
  AND o.is_active = true;

-- =============================================
-- 9. 測試使用者
-- =============================================


-- 一般使用者 (3 個)
INSERT INTO APP_USER (user_name, user_phone, user_email, password_hash, is_active) VALUES 
-- ✅ 修正：username → user_name, phone → user_phone, email → user_email
('alice_wang', '0911111111', 'alice@example.com', '$2b$12$vy.qEbovynCopDpdr74R1u8FlKIVDgkOAOXZ6GV/KQ5aQ6HigwUjW', true),  -- 密碼: aaa111
('bob_chen', '0922222222', 'bob@example.com', '$2b$12$rG6HCjlGaUqiRzLnTzhthOGukEsr0o9RuOw03kkjXoxLdekyOIuta', true),    -- 密碼: bbb222
('carol_liu', '0933333333', 'carol@example.com', '$2b$12$QAejoRQXEKHNtV04iyWpiOTVXAPT3zbEihikwHyn7HmlTBO6.oWWy', true);  -- 密碼: ccc333

-- 門市人員 (1 個 - 負責 50嵐公館店)
INSERT INTO APP_USER (user_name, user_phone, user_email, password_hash, is_active) VALUES 
('staff_50lan', '0945678901', 'staff@50lan.com', '$2b$12$kx2l7KR5M/NFYBnINETxsOPLiFbjLeHAT9JpjkqtYa0TT1Jzw6iAe', true);  -- 密碼: staff123

-- 品牌管理者 (1 個 - 負責 50嵐品牌)
INSERT INTO APP_USER (user_name, user_phone, user_email, password_hash, is_active) VALUES 
('manager_50lan', '0956789012', 'manager@50lan.com', '$2b$12$kkG0Q1dL/vqfn09KiDsVJOvXB7hRyS0bI0tjS7FJjH9XWv4O/mJEe', true);  -- 密碼: manager123

-- aaa111: $2b$12$vy.qEbovynCopDpdr74R1u8FlKIVDgkOAOXZ6GV/KQ5aQ6HigwUjW
-- bbb222: $2b$12$rG6HCjlGaUqiRzLnTzhthOGukEsr0o9RuOw03kkjXoxLdekyOIuta
-- ccc333: $2b$12$QAejoRQXEKHNtV04iyWpiOTVXAPT3zbEihikwHyn7HmlTBO6.oWWy
-- staff123: $2b$12$kx2l7KR5M/NFYBnINETxsOPLiFbjLeHAT9JpjkqtYa0TT1Jzw6iAe
-- manager123: $2b$12$kkG0Q1dL/vqfn09KiDsVJOvXB7hRyS0bI0tjS7FJjH9XWv4O/mJEe

-- =============================================
-- 10. 使用者角色分配
-- =============================================

-- 一般使用者角色 (user_id 1, 2, 3 -> role_id 1: member)
INSERT INTO USER_ROLE_ASSIGNMENT (user_id, role_id, scope_type, brand_id, store_id) VALUES 
(1, 1, 'global', NULL, NULL),  -- alice_wang: member
(2, 1, 'global', NULL, NULL),  -- bob_chen: member
(3, 1, 'global', NULL, NULL);  -- carol_liu: member

-- 門市人員角色 (user_id 4 -> role_id 2: store_staff, 管理 store_id 2)
INSERT INTO USER_ROLE_ASSIGNMENT (user_id, role_id, scope_type, brand_id, store_id) VALUES 
(4, 2, 'store', NULL, 2);  -- staff_50lan: 50嵐公館店的門市人員

-- 品牌管理者角色 (user_id 5 -> role_id 3: brand_manager, 管理 brand_id 2)
INSERT INTO USER_ROLE_ASSIGNMENT (user_id, role_id, scope_type, brand_id, store_id) VALUES 
(5, 3, 'brand', 2, NULL);  -- manager_50lan: 50嵐品牌管理者

-- =============================================
-- 11. 測試地址資料
-- =============================================

-- 為一般使用者新增常用地址
INSERT INTO USER_ADDRESS (user_id, district, label, address) VALUES 
-- alice_wang 的地址
(1, '大安區', '家', '台北市大安區羅斯福路三段283巷3號'),

-- bob_chen 的地址
(2, '永和區', '公司',  '新北市永和區中正路100號'),

-- carol_liu 的地址
(3, '中正區', '家', '台北市中正區汀州路三段200號')


-- =============================================
-- 12. 驗證資料
-- =============================================

-- SELECT '=== 驗證結果 ===' as status;
-- SELECT 'BRAND' as table_name, COUNT(*) as count FROM BRAND
-- UNION ALL SELECT 'STORE', COUNT(*) FROM STORE
-- UNION ALL SELECT 'PRODUCT', COUNT(*) FROM PRODUCT
-- UNION ALL SELECT 'STORE_PRODUCT', COUNT(*) FROM STORE_PRODUCT
-- UNION ALL SELECT 'OPTION_CATEGORY', COUNT(*) FROM OPTION_CATEGORY
-- UNION ALL SELECT 'OPTION', COUNT(*) FROM OPTION
-- UNION ALL SELECT 'BRAND_PRODUCT_OPTION_RULE', COUNT(*) FROM BRAND_PRODUCT_OPTION_RULE
-- UNION ALL SELECT 'STORE_OPTION', COUNT(*) FROM STORE_OPTION
-- UNION ALL SELECT 'APP_USER', COUNT(*) FROM APP_USER
-- UNION ALL SELECT 'USER_ROLE_ASSIGNMENT', COUNT(*) FROM USER_ROLE_ASSIGNMENT
-- UNION ALL SELECT 'USER_ADDRESS', COUNT(*) FROM USER_ADDRESS;