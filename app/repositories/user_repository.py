###################################
# -----usersテーブルへのSQL処理-----
###################################

# ログインIDに対応するアカウント情報w取得する
def find_by_login_id(connection, login_id):
    cursor = connection.cursor(dictionary=True, buffered=True)

    try:
        # ログインの判定と、ログイン状態の管理に必要な項目を取得する
        sql = """
            SELECT user_id, user_name, login_id, password_hash, role, is_active, must_change_password, session_version
            FROM users
            WHERE login_id_key = LOWER(%s)
            LIMIT 1
            """

        cursor.execute(sql, (login_id,))

        return cursor.fetchone()

    finally:
        cursor.close()