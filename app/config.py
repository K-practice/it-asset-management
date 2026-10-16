#############################################
# -----.envの場所の特定・存在確認・読み込み-----
#############################################

from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    # プロジェクト直下の.envを環境変数に読み込む。
    env_path = Path(__file__).resolve().parents[1] / ".env"

    # 存在確認
    if not env_path.is_file():
        raise ValueError("プロジェクト直下に.envがありません。")

    # 読み込みオプション
    load_dotenv(
        dotenv_path=env_path,
        override=False,
        interpolate=False,
        encoding="utf-8"
    )