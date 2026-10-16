---------------------------
-- 採番管理の初期データ登録
---------------------------

-- 使用するデータベース
USE it_asset_management;

-- 接続の時刻設定
SET SESSION time_zone = '+09:00';

-- 種別別採番管理の初期データ
INSERT INTO asset_number_sequences(asset_type, last_number)
            VALUES(1,0),(2,0);