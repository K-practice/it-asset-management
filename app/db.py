############################
# -----DB接続関数ファイル-----
############################

import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv


def get_connection(*, autocommit=False):
    # * : 後ろの引数を、名前付きで指定させる
    # autocommit=False : 省略時は自動コミットを無効にする

    # 環境変数の設定を使い、新しいDB接続を作成して返す。
    db_user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")

    if not db_user or not db_name:
        raise ValueError("DB_USERとDB_NAMEを設定してください。")

    try:
        db_port = int(os.getenv("DB_PORT", "3306"))
    except ValueError:
        raise ValueError("DB_PORTは整数で設定してください") from None

    if not 1 <= db_port <= 65535:
        raise ValueError("DB_PORTは1~65535で設定してください。")

    return mysql.connector.connect(
        host = os.getenv("DB_HOST", "127.0.0.1"),
        port = db_port,
        user = db_user,
        password = os.getenv("DB_PASSWORD", ""),
        database = db_name,
        charset = os.getenv("DB_CHARSET", "utf8mb4"),
        collation = os.getenv("DB_COLLATION", "utf8mb4_bin"),
        time_zone = os.getenv("DB_TIME_ZONE", "+09:00"),
        use_pure = True,
        connection_timeout = 5,
        autocommit = autocommit,
    )