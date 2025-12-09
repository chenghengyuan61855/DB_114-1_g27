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
(1, '輕纖穀奈茶', '零咖啡因、輕盈無負擔的穀物茶', true),
(1, '雪藏紅茶', '香草冰淇淋與經典濃厚紅茶的綿綿情意', true),
(1, '胭脂多多', '兒時記憶裡的多多碰上熟後的蜜桃風味', true),
(1, '白玉歐蕾', '醇厚鮮奶茶咀嚼著Q彈白透珍珠', true),
(1, '熟檸紅茶', '經典熟成紅茶與100%台灣在地檸檬原汁', true),
(1, '胭脂紅茶', '絲絨般果香調與一抹蜜桃風味', true),
(1, '白玉奶茶', '台灣經典珍珠奶茶', true),
(1, '春芽冷露', '青翠綠茶與古法熬煮冬瓜露', true),
(1, '熟成紅茶', '帶有濃穩果香的經典紅茶', true),
(1, '春梅冰茶', '春梅與冬瓜相遇', true);

-- 50嵐 (product_id 11~20)
INSERT INTO PRODUCT (brand_id, product_name, product_description, is_active) VALUES 
(2, '四季春青茶', '順口回甘，經典好茶', true),
(2, '黃金烏龍', '香氣濃郁的烏龍茶', true),
(2, '8冰綠', '金桔汁與梅汁搭配綠茶', true),
(2, '冰淇淋紅茶', '香草冰淇淋加上紅茶', true),
(2, '波霸奶茶', '大顆珍珠搭配奶茶', true),
(2, '珍珠奶茶', '小顆珍珠搭配奶茶', true),
(2, '四季春珍波椰', '四季春加珍珠波霸椰果，超滿足', true),
(2, '茉莉綠茶', '清新茉莉香氣綠茶', true), 
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
(4, '芋泥波波鮮奶2.0', '大甲芋頭加珍珠鮮奶', true),
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
(5, '焙香決明大麥', '自帶甜味的大麥茶', true), -- 名稱修正
(5, '青檸香茶', '手搖檸檬皮香氣', true),
(5, '柳丁綠茶', '台灣柳丁汁加綠茶', true);

-- =============================================
-- 4. 門市商品定價
-- =============================================

-- 可不可 — Top 10 推薦必喝
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(1, 1, 50, true),  -- 輕纖穀奈茶
(1, 2, 60, true),  -- 雪藏紅茶
(1, 3, 60, true),  -- 胭脂多多
(1, 4, 70, true),  -- 白玉歐蕾
(1, 5, 55, true),  -- 熟檸紅茶
(1, 6, 50, true),  -- 胭脂紅茶
(1, 7, 60, true),  -- 白玉奶茶
(1, 8, 45, true),  -- 春芽冷露
(1, 9, 40, true),  -- 熟成紅茶
(1, 10, 60, true); -- 春梅冰茶

-- 50嵐_公館 (Store ID 2)
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(2, 11, 40, true), (2, 12, 40, true), (2, 13, 60, true), (2, 14, 60, true), (2, 15, 60, true),
(2, 16, 60, true), (2, 17, 50, true), (2, 18, 40, true), (2, 19, 40, true), (2, 20, 60, true);

-- 50嵐_復興店 (Store ID 3)
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(3, 11, 40, true), (3, 12, 40, true), (3, 13, 60, true), (3, 14, 60, true), (3, 15, 60, true),
(3, 16, 60, true), (3, 17, 50, true), (3, 18, 40, true), (3, 19, 40, true), (3, 20, 60, true);

-- 50嵐_永康店 (Store ID 4)
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(4, 11, 40, true), (4, 12, 40, true), (4, 13, 60, true), (4, 14, 60, true), (4, 15, 60, true),
(4, 16, 60, true), (4, 17, 50, true), (4, 18, 40, true), (4, 19, 40, true), (4, 20, 60, true);

-- 50嵐_同安店 (Store ID 5)
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(5, 11, 40, true), (5, 12, 40, true), (5, 13, 60, true), (5, 14, 60, true), (5, 15, 60, true),
(5, 16, 60, true), (5, 17, 50, true), (5, 18, 40, true), (5, 19, 40, true), (5, 20, 60, true);

-- 50嵐_通化店 (Store ID 6)
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(6, 11, 40, true), (6, 12, 40, true), (6, 13, 60, true), (6, 14, 60, true), (6, 15, 60, true),
(6, 16, 60, true), (6, 17, 50, true), (6, 18, 40, true), (6, 19, 40, true), (6, 20, 60, true);

-- 得正
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(7, 21, 35, true), -- 春烏龍 (L:35)
(7, 22, 35, true), -- 輕烏龍 (L:35)
(7, 23, 35, true), -- 焙烏龍 (L:35)
(7, 24, 65, true), -- 檸檬春烏龍 (L:65) - 原 SQL 55 錯誤
(7, 25, 60, true), -- 芝士奶蓋春烏龍 (L:60)
(7, 26, 50, true), -- 焙烏龍奶茶 (L:50)
(7, 27, 65, true), -- 焙烏龍鮮奶 (L:65) - 原 SQL 60 錯誤
(7, 28, 65, true), -- 優酪春烏龍 (L:65) - 原 SQL 55 錯誤
(7, 29, 70, true), -- 甘蔗春烏龍 (L:70) - 原 SQL 55 錯誤
(7, 30, 60, true); -- 黃金珍珠奶綠 (L:60) - 原 SQL 55 錯誤

-- 麻古
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(8, 31, 35, true), -- 高山金萱茶 (L:35)
(8, 32, 40, true), -- 翡翠綠茶 (L:40) - 原 SQL 35 錯誤
(8, 33, 90, true), -- 楊枝甘露2.0 (L:90) - 原 SQL 80 錯誤
(8, 34, 95, true), -- 芝芝葡萄果粒 (L:95) - 原 SQL 90 錯誤
(8, 35, 80, true), -- 柳橙果粒茶 (L:80) - 原 SQL 75 錯誤
(8, 36, 75, true), -- 番茄梅蜜 (L:75) - 原 SQL 70 錯誤
(8, 37, 90, true), -- 芋泥波波鮮奶2.0 (L:90) - 原 SQL 85 錯誤
(8, 38, 70, true), -- 波霸紅茶拿鐵 (L:70) - 原 SQL 60 錯誤
(8, 39, 85, true), -- 香橙果粒茶 (L:85) - 原 SQL 75 錯誤
(8, 40, 45, true); -- 金萱雙Q (L:45) - 原 SQL 50 錯誤


-- 迷客夏
INSERT INTO STORE_PRODUCT (store_id, product_id, price, is_active) VALUES 
(9, 41, 65, true), -- 大正紅茶拿鐵 (L:65) 
(9, 42, 65, true), -- 伯爵紅茶拿鐵 (L:65) 
(9, 43, 75, true), -- 珍珠紅茶拿鐵 (L:75) 
(9, 44, 90, true), -- 芋頭鮮奶 (L:90) 
(9, 45, 85, true), -- 手炒黑糖鮮奶 (L:85) 
(9, 46, 40, true), -- 原片初露青茶 (L:40) 
(9, 47, 40, true), -- 琥珀高峰烏龍 (L:40) 
(9, 48, 35, true), -- 焙香決明大麥 (L:35) 
(9, 49, 70, true), -- 青檸香茶 (L:70) 
(9, 50, 70, true); -- 柳丁綠茶 (L:70)

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
(3, '加白玉珍珠', 10, true),(3, '加水玉珍珠', 10, true),(3, '加墨玉', 15, true),(3, '加春梅凍', 15, true),(3, '加榛果燕麥凍', 15, true),
(6, '加波霸', 10, true),(6, '加椰果', 10, true),(6, '加珍珠', 10, true),(6, '加燕麥', 10, true),
(9, '加珍珠', 10, true),(9, '加黃金珍珠', 10, true),(9, '加焙烏龍茶凍', 10, true),
(12, '加芝芝（超好喝！）', 20, true),(12, '加波霸', 10, true),(12, '加椰果', 10, true),(12, '加養樂多', 10, true),
(15, '加珍珠', 10, true),(15, '加綠茶凍', 10, true),(15, '加桂香粉粿', 15, true);

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
(3, '中正區', '家', '台北市中正區汀州路三段200號');


-- =============================================
-- 13. 新增營業時間
-- =============================================

-- 檢查目前哪些門市沒有營業時間
SELECT s.store_id, s.store_name, COUNT(sh.store_id) as hours_count
FROM STORE s
LEFT JOIN STORE_HOURS sh ON s.store_id = sh.store_id
GROUP BY s.store_id, s.store_name
HAVING COUNT(sh.store_id) = 0;

-- 為所有沒有營業時間的門市初始化
-- weekday: 0=週一, 1=週二, 2=週三, 3=週四, 4=週五, 5=週六, 6=週日
INSERT INTO STORE_HOURS (store_id, weekday, is_open, open_time, close_time)
SELECT 
    s.store_id,
    w.weekday,
    true as is_open,
    '10:00:00'::time as open_time,
    '22:00:00'::time as close_time
FROM STORE s
CROSS JOIN (
    SELECT 0 as weekday UNION ALL
    SELECT 1 UNION ALL
    SELECT 2 UNION ALL
    SELECT 3 UNION ALL
    SELECT 4 UNION ALL
    SELECT 5 UNION ALL
    SELECT 6
) w
WHERE NOT EXISTS (
    -- 只新增那些還沒有任何營業時間記錄的門市
    SELECT 1 FROM STORE_HOURS sh 
    WHERE sh.store_id = s.store_id
);

-- 驗證：檢查所有門市的營業時間記錄數（應該都是 7 天）
SELECT 
    s.store_id, 
    s.store_name, 
    COUNT(sh.store_id) as hours_count
FROM STORE s
LEFT JOIN STORE_HOURS sh ON s.store_id = sh.store_id
GROUP BY s.store_id, s.store_name
ORDER BY s.store_id;

-- 查看初始化結果
SELECT 
    s.store_id,
    s.store_name,
    sh.weekday,
    CASE sh.weekday
        WHEN 0 THEN '週一'
        WHEN 1 THEN '週二'
        WHEN 2 THEN '週三'
        WHEN 3 THEN '週四'
        WHEN 4 THEN '週五'
        WHEN 5 THEN '週六'
        WHEN 6 THEN '週日'
    END as weekday_name,
    sh.is_open,
    sh.open_time,
    sh.close_time
FROM STORE s
JOIN STORE_HOURS sh ON s.store_id = sh.store_id
ORDER BY s.store_id, sh.weekday;


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