#######################
# -----設定とルート-----
#######################

import os
from flask import Flask
from app.config import load_environment

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

    # URLごとの処理をまとめたBlueprintを読み込む
    from app.routes.main import bp

    # Blueprintに定義したルートをFlaskアプリに登録する
    app.register_blueprint(bp)

    # 設定が完了したFlaskアプリを呼び出し元に返す
    return app
