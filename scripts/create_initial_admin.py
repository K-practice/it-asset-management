#####################################################################
# -----有効な管理担当者が存在しない場合のみ管理担当者を1人作成する処理-----
#####################################################################

# 正規表現を扱う
import re
# 警告の扱いを制御する
import warnings
# 特定の例外を制御する
from contextlib import suppress
# パスワードを非表示で入力する
from getpass import GetPassWarning, getpass
# DBと通信する
import mysql.connector
# パスワードをハッシュ化する
from werkzeug.security import generate_password_hash
# 環境設定共通関数
from app.config import load_environment
# DB接続共通関数
from app.db import get_connection

def main():
    # 接続前にエラーが発生した場合にも、終了処理を出来るようにする
    connection = None
    cursor = None

    try:
        # 1. 共通関数で環境設定を読み込み、DBへ接続する
        load_environment()
        connection = get_connection(autocommit=True)

        # 結果を辞書で取得し、検索結果を先読みする
        cursor = connection.cursor(dictionary=True, buffered=True)

        # 2. このスクリプトを同じDBで同時実行しないためのロック
        # 接続中のDB名を使い、DBごとにロック名を分ける
        lock_name = f"{connection.database}:create_initial_admin"

        cursor.execute(
            "SELECT GET_LOCK(%s, 0) AS acquired",
            (lock_name,),
            )
        lock_result = cursor.fetchone()

        # 1以外は、使用中または取得失敗なので中止する
        if lock_result is None or lock_result["acquired"] != 1:
            raise ValueError("初期作成用のロックを取得できませんでした。")

        # 3. 有効な管理担当者が存在しない場合は、新規作成しない
        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE role = 2 AND is_active = 1
            LIMIT 1
            """
        )

        if cursor.fetchone() is not None:
            print("有効な管理担当者が存在するため、作成しません。")
            return 0

        # 4. 社員名とログインIDを入力・検証する
        user_name = input("社員名").strip()
        login_id = input("ログインID:")

        if not 1 <= len(user_name) <= 100:
            raise ValueError("社員名は1~100文字で入力してください。")

        if re.fullmatch(r"[A-Za-z0-9._-]{1,64}", login_id) is None:
            raise ValueError("ログインIDは半角英数字と「.」「_」「-」のみ、1~64文字です。")

        # 無効なアカウントを含めて、同じログインIDの登録を防ぐ
        cursor.execute(
            "SELECT user_id FROM users WHERE login_id_key = LOWER(%s)",
            (login_id,),
        )

        if cursor.fetchone() is not None:
            raise ValueError("このログインIDは既に登録されています。")

        # 5. パスワードを非表示で入力する
        # 非表示入力に対応していない環境では、入力せずに中止する
        warnings.simplefilter("error", GetPassWarning)
        password = getpass("初期パスワード(15~64文字):")

        if not 15 <= len(password) <=64:
            raise ValueError("パスワードは15~64文字で入力してください。")

        password_confirm = getpass("初期パスワード（確認）: ")

        if password != password_confirm:
            raise ValueError("確認用パスワードが一致しません。")

        # 平文のパスワードを、保存用のハッシュ文字列に変換する
        password_hash = generate_password_hash(password, method="scrypt")

        # 6. ここから登録用のトランザクションを開始する
        connection.start_transaction()

        # 権限・有効状態・初回変更必須・版数は初期管理者用に固定する
        sql = """
            INSERT INTO users (
                user_name,
                login_id,
                login_id_key,
                password_hash,
                role,
                is_active,
                must_change_password,
                session_version
            )
            VALUES (%s, %s, LOWER(%s), %s, 2, 1, 1, 1)
        """

        # 入力値はSQLに直接連結せず、プレースホルダーへ渡す
        # login_idは、表示用と小文字キー用の2か所に渡す
        cursor.execute(
            sql,
            (user_name, login_id, login_id, password_hash),
        )

        # 自動採番された社員IDを取得してから、登録を確定する
        user_id = cursor.lastrowid
        connection.commit()

        # パスワードやハッシュ文字列は表示しない
        print("初期管理担当者を作成しました。")
        print(f"社員ID: {user_id}")
        print(f"ログインID: {login_id}")
        return 0

    except GetPassWarning:
        print("パスワードを非表示で入力できるターミナルで実行してください。")
        return 1

    except ValueError as error:
        # 環境設定・入力内容・実行条件に関するエラー
        print(f"設定・入力エラー: {error}")
        return 1

    except mysql.connector.Error as error:
        # DB接続やSQL実行のエラー
        # エラーの種類
        print(f"エラーの種類:{type(error).__name__}")
        # エラー番号
        print(f"エラー番号:{error.errno}")
        # 具体的なエラーメッセージ
        print(f"詳細:{error.msg}")
        # DB側のエラー分類
        print(f"SQLSTATE:{error.sqlstate}")

        return 1

    except (KeyboardInterrupt, EOFError):
        # Ctrl+Cや入力の終了で中止された場合
        print("\n作成を中止しました。")
        return 1

    finally:
        # 未確定の登録処理があれば取り消す
        if connection is not None:
            with suppress(mysql.connector.Error):
                if connection.in_transaction:
                    connection.rollback()

        # 終了処理のDBエラーで、後続の終了処理を止めない
        if cursor is not None:
            with suppress(mysql.connector.Error):
                cursor.close()

        # 接続を閉じると、GET_LOCKで取得したロックも解放される
        if connection is not None:
            with suppress(mysql.connector.Error):
                connection.close()


# モジュールとして実行された場合に、main()を呼び出す
if __name__ == "__main__":
    # 0は正常終了、1はエラーまたは中止
    raise SystemExit(main())