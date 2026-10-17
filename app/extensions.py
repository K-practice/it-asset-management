###################################
# -----Flaskの拡張機能を共通管理-----
###################################

from flask_wtf.csrf import CSRFProtect

# CSRF対策を担当する拡張機能を作成
csrf = CSRFProtect()