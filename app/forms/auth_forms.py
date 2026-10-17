####################################################
# -----ログインフォームン項目・入力ルールを定義する-----
####################################################

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp

# ログイン画面の入力項目と入力ルールを定義する
class LoginForm(FlaskForm):

    # ログインIDの入力欄
    login_id = StringField(
        # 画面表示項目名
        "ログインID",
        # 入力内容を確認するルール
        validators=[
            # 未入力を拒否する
            InputRequired(
                message = "ログインIDを入力してください。"
            ),
            # 文字数を確認する
            Length(
                min=1,
                max=64,
                message="ログインIDは1~64文字で入力してください。",
            ),
            # 半角英数字と「.」「_」「-」のみ許可する
            Regexp(
                r"[A-Za-z0-9._-]+\Z",
                message = "ログインIDは半角英数字と「.」「_」「-」のみ使用できます。",
            ),
        ],

        # HTMLの入力欄につける属性
        render_kw={
            # ブラウザにログインIDの入力欄であることを伝える
            "autocomplete": "username",
            # スマートフォンなどでの自動大文字化を抑制する
            "autocapitalize": "none",
            # スペルチェックを無効にする
            "spellcheck": "false"
        },
    )

    # パスワードの入力欄
    password = PasswordField(
        "パスワード",
        validators=[
            # 未入力を拒否する
            InputRequired(
                message = "パスワードを入力してください。",
            ),
            # 認証処理と同じ文字数制限を使用
            Length(
                min=15,
                max=64,
                message = "パスワードは15~64文字で入力してください。",
            ),
        ],

        render_kw={
            "autocomplete": "current-password",
        },
    )

    # ログイン実行送信ボタン
    submit = SubmitField("ログイン")
