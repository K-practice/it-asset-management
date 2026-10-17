##############################
# -----起動確認用URLの処理-----
##############################

# URLごとの処理を、機能別のファイルにまとめる
from flask import Blueprint

# URLと、そのURLにアクセスした際の処理をまとめる
# 第1引数の"main"は、このBlueprintの名前
# 第2引数の__name__は、現在のモジュール名
bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET"])
def index():
    return "IT資産管理システム:Flaskアプリが正常に起動しました。"