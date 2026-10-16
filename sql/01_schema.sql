-- DB・テーブル・制約の作成

-- データベース作成
CREATE DATABASE IF NOT EXISTS it_asset_management
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_bin;

-- 接続の時刻設定を日本時間にする
SET SESSION time_zone = '+09:00';

-- 使用するデータベースの選択
USE it_asset_management;

-- usersテーブル
CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    login_id VARCHAR(64) NOT NULL,
    login_id_key VARCHAR(64) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role INT NOT NULL DEFAULT 1,
    is_active INT NOT NULL DEFAULT 1,
    must_change_password INT NOT NULL DEFAULT 1,
    session_version INT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- CHECK制約
    CHECK(CHAR_LENGTH(TRIM(user_name)) >= 1),
    CHECK(
        CHAR_LENGTH(login_id) >= 1
        AND login_id NOT REGEXP '[^A-Za-z0-9._-]'
    ),
    CHECK(BINARY login_id_key = BINARY LOWER(login_id)),
    CHECK(CHAR_LENGTH(TRIM(password_hash)) >= 1),
    CHECK(role IN(1, 2)),
    CHECK(is_active IN(0, 1)),
    CHECK(must_change_password IN(0, 1)),
    CHECK(session_version >= 1)
);

-- locationsテーブル
CREATE TABLE locations (
    location_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL UNIQUE,
    is_active INT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- CHECK制約
    CHECK(CHAR_LENGTH(TRIM(location_name)) >= 1),
    CHECK(is_active IN(0, 1))
);

-- asset_number_sequencesテーブル
CREATE TABLE asset_number_sequences (
    asset_type INT NOT NULL PRIMARY KEY,
    last_number INT NOT NULL DEFAULT 0,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- CHECK制約
    CHECK(asset_type IN(1, 2)),
    CHECK(last_number >= 0)
);

-- assetsテーブル
CREATE TABLE assets (
    asset_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    asset_type INT NOT NULL,
    sequence_number INT NOT NULL UNIQUE,
    management_number VARCHAR(20) NOT NULL UNIQUE,
    asset_name VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100),
    model_number VARCHAR(100),
    serial_number VARCHAR(100),
    location_id INT NOT NULL,
    location_detail VARCHAR(255),
    assignment_type INT NOT NULL UNIQUE,
    assigned_user_id INT,
    status INT NOT NULL,
    notes VARCHAR(1000),
    is_deleted INT NOT NULL DEFAULT 0,
    row_version INT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- CHECK制約
    CHECK(asset_type IN(1, 2)),
    CHECK(sequence_number >= 1),
    CHECK(
        BINARY management_number = BINARY CONCAT(
            CASE asset_type
                WHEN 1 THEN 'PC-'
                WHEN 2 THEN 'NET-'
            END,
            LPAD(
                sequence_number,
                GREATEST(6, CHAR_LENGTH(sequence_number)),
                '0'
            )
        )
    ),
    CHECK(CHAR_LENGTH(TRIM(asset_name)) >= 1),
    CHECK(manufacturer IS NULL OR CHAR_LENGTH(TRIM(manufacturer)) >= 1),
    CHECK(model_number IS NULL OR CHAR_LENGTH(TRIM(model_number)) >= 1),
    CHECK(serial_number IS NULL OR CHAR_LENGTH(TRIM(serial_number)) >= 1),
    CHECK(location_detail IS NULL OR CHAR_LENGTH(TRIM(location_detail)) >= 1),
    CHECK(assignment_type IN(1, 2, 3)),
    CHECK(
        (assignment_type = 1 AND assigned_user_id IS NOT NULL)
        OR
        (assignment_type IN(2, 3) AND assigned_user_id IS NULL)
    ),
    CHECK(status IN(1, 2, 3, 4)),
    CHECK(
        (status <> 1 OR assignment_type IN(1, 2))
        AND
        (status <> 4 OR assignment_type = 3)
    ),
    CHECK(notes IS NULL OR CHAR_LENGTH(TRIM(notes)) >= 1),
    CHECK(is_deleted IN(0, 1)),
    CHECK(row_version >= 1),

    -- 外部キー制約
    FOREIGN KEY (asset_type)
    REFERENCES asset_number_sequences(asset_type)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,

    FOREIGN KEY (location_id)
    REFERENCES locations(location_id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,

    FOREIGN KEY (assigned_user_id)
    REFERENCES users(user_id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT
);

-- asset_change_historiesテーブル
CREATE TABLE asset_change_histories (
    history_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    asset_id INT NOT NULL,
    change_type INT NOT NULL,
    before_value VARCHAR(512) NOT NULL,
    after_value VARCHAR(512) NOT NULL,
    changed_by_user_id INT NOT NULL,
    changed_by_name VARCHAR(100) NOT NULL,
    changed_by_login_id VARCHAR(64) NOT NULL,
    changed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- CHECK制約
    CHECK(change_type IN(1, 2, 3, 4, 5)),
    CHECK(CHAR_LENGTH(TRIM(before_value)) >= 1),
    CHECK(CHAR_LENGTH(TRIM(after_value)) >= 1),
    CHECK(CHAR_LENGTH(TRIM(changed_by_name)) >= 1),
    CHECK(
        CHAR_LENGTH(changed_by_login_id) >= 1
        AND changed_by_login_id NOT REGEXP '[^A-Za-z0-9._-]'
    ),

    -- 外部キー制約
    FOREIGN KEY (asset_id)
    REFERENCES assets(asset_id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,

    FOREIGN KEY (changed_by_user_id)
    REFERENCES users(user_id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT
);