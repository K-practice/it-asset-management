#############################################
# -----ログイン情報を確認し、認証結果を返す-----
#############################################

import re
from contextlib import closing
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_connection
from app.repositories.user_repository import find_by_login_id

# アカウントが存在しない場合の、照合結果に使用するダミーハッシュ
_DUMMY_PASSWORD_HASH = generate_password_hash(
    "dummy-password-for-login-check",
    method="scrypt",
)

# ログインIDとパスワードでアカウント認証をする。
def authenticate_user(login_id, password):

    # ログインIDが決定済みの形式にあっているか確認
    if re.fullmatch(r"[A-Za-z0-9._-]{1,64}", login_id) is None:
        return None

    # パスワードの文字数確認
    if not 15 <= len(password) <= 64:
        return None

    # 読み取り用DB接続を作成
    with closing(get_connection(autocommit=True)) as connection:
        user = find_by_login_id(connection, login_id)

    if user is None:
        # 未登録のIDでも、パスワード照合の処理を実行する
        password_hash = _DUMMY_PASSWORD_HASH
    else:
        # 登録済みの場合は、DBに保存されたハッシュを使用する
        password_hash = user["password_hash"]

    # 入力されたパスワードと、保存済みハッシュが対応するか確認
    password_matches = check_password_hash(password_hash, password)

    # 未登録のIDは認証失敗
    if user is None:
        return None

    # パスワードが一致しなければ認証失敗
    if not password_matches:
        return None

    # 無効化されたアカウントは、パスワードが正しくても認証失敗
    if user["is_active"] != 1:
        return None

    # 認証に成功した場合、必要な情報だけを返す
    return{
        "user_id": user["user_id"],
        "user_name": user["user_name"],
        "login_id": user["login_id"],
        "role": user["role"],
        "must_change_password": user["must_change_password"],
        "session_version": user["session_version"]
    }
