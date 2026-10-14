########################################
# -----DB接続を確認するPythonファイル-----
########################################
# ファイルやフォルダ―の場所を扱う
from pathlib import Path
# 環境設定から設定値を取得
import os
# .envの設定ファイルを読み込む
from dotenv import load_dotenv
# DB接続・SQL実行などを行う
import mysql.connector

# -----DB接続確認処理-----
def main():

    # DBとの接続を管理する変数
    connection = None
    # SQLを実行し、結果を取得する変数
    cursor = None

    try :
        # ---1. 作品フォルダー直下の.envを読み込む---
        # check_db.pyのパスを取得し、絶対パスにして代入
        project_dir = Path(__file__).resolve().parents[1]
        env_path = project_dir / ".env"

        # ファイルの存在を確認し、読み込む
        if not env_path.is_file():
            # 「設定に問題がある」と判断し、後ろのexcept ValueErrorへ処理を移す
            raise ValueError("作品フォルダー直下に.envがありません。")
        load_dotenv(env_path, interpolate = False)

        # ---2. 接続設定を取得する---
        # 接続情報を取得し、入力を確認する
        db_user = os.getenv("DB_USER")
        db_port = int(os.getenv("DB_PORT", "3306"))

        if not db_user:
            raise ValueError(".envのDB_USERを設定してください")

        if not 1 <= db_port <= 65535:
            raise ValueError("DB_PORTは1~65535で設定してください。")

        # 3. MariaDBサーバーへ接続する
        connection = mysql.connector.connect(
            host = os.getenv("DB_HOST", "127.0.0.1"),
            port = db_port,
            user = db_user,
            password = os.getenv("DB_PASSWORD", ""),
            charset = os.getenv("DB_CHARSET", "utf8mb4"),
            # 接続で使う照合順序
            collation = os.getenv("DB_COLLATION", "utf8mb4-bin"),
            # 接続セッションのタイムゾーン
            time_zone = os.getenv("DB_TIME_ZONE", "+09:00"),
            # ライブラリのPython実装を使用する
            use_pure = True,
            # 接続処理のタイムアウトを5秒にする
            connection_timeout = 5,
        )

        # 4. 確認用SQLを実行する
        cursor = connection.cursor(dictionary=True)

        sql = """
            SELECT
                VERSION() AS server_version,
                @@character_set_connection AS connection_charset,
                @@collation_connection AS connection_collation,
                @@session.time_zone AS session_time_zone
            """
        # @@character_set_connection : 接続で使われている文字コード
        # @@collation_connection : 接続で使われている照合順序
        # @@session.time_zone : 現在の接続のタイムゾーン

        cursor.execute(sql)
        result = cursor.fetchone()

        if result is None:
            raise ValueError("確認用SQLの結果を取得できませんでした。")

        # 5. 結果を表示する
        print("DB接続に成功しました。")

        for name, value in result.items():
            # 変数の値を埋め込んで出力
            print(f"{name}: {value}")

        # 正常終了
        return 0

    except ValueError as error:
        print(f"設定・確認エラー: {error}")

        # 失敗
        return 1

    except mysql.connector.Error as error:
        print(f"DB接続・SQLエラー: {error.errno}")
        print(error.msg)

        return 1

    finally:
        # 6. 作成できたカーソルと接続を閉じる
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

if __name__ == "__main__":
    # main()の戻り値を使ってプログラムを終了
    raise SystemExit(main())




