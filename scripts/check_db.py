########################################
# -----DB接続を確認するPythonファイル-----
########################################

# 終了処理で発生した特定の例外を抑制する
from contextlib import suppress
# DB関連の例外を補足する
import mysql.connector
# DB接続共通関数
from app.db import get_connection
# .envを読み込む共通関数
from app.config import load_environment


# -----DB接続確認処理-----
def main():

    # DBとの接続を管理する変数
    connection = None
    # SQLを実行し、結果を取得する変数
    cursor = None

    try :
        # 1. .envの環境変数を読み込む
        load_environment()

        # 2. DB接続を作成する
        connection = get_connection()
        # 3. 取得結果をカラム名で参照できるようにする
        cursor = connection.cursor(dictionary=True)

        # 4. 確認用SQLを実行する
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
        # 接続が作成され、未確定のトランザクションがある場合は取り消す
        if connection is not None:
            with suppress(mysql.connector.Error):
                if connection.in_transaction:
                    connection.rollback()
        # 作成できたカーソルと接続を閉じる
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

if __name__ == "__main__":
    # main()の戻り値を使ってプログラムを終了
    raise SystemExit(main())




