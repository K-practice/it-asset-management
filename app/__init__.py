#######################
# -----設定とルート-----
#######################

import os
from flask import Flask
from flask_wtf.csrf import CSRFError
from app.config import load_environment
from app.extensions import csrf

# 設定とルートを登録したFlaskアプリを作成して返す
def create_app():
    load_environment()

    app = Flask(__name__)

    secret_key = os.getenv("SECRET_KEY")

    # 未設定・空文字・見本のままの場合は起動を止める
    if not secret_key or secret_key == "replace-with-local-secret":
        raise ValueError(".envのSECRET_KEYに、このプロジェクト用の秘密鍵を設定してください。")

    # Flaskアプリの設定として秘密鍵を登録する
    app.config["SECRET_KEY"] = secret_key

    # FlaskアプリにCSRF対策を登録する
    csrf.init_app(app)

    # CSRFトークン不足・不一致・期限切れなどを処理する
    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        # CSRF検証に失敗した場合、日本語の案内を返す
        return (
            "送信内容を確認できませんでした。"
            "画面を再読み込みして、もう一度操作してください。",
            400,
        )

    # URLごとの処理をまとめたBlueprintを読み込む
    from app.routes.main import bp

    # Blueprintに定義したルートをFlaskアプリに登録する
    app.register_blueprint(bp)

    # 設定が完了したFlaskアプリを呼び出し元に返す
    return app
