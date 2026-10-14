## 使用技術一覧
<!-- 使用技術のバッジ -->
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-663399?style=for-the-badge&logo=css&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

## 目次
1. [概要](#概要)
2. [実装予定の機能](#実装予定の機能)
3. [開発環境](#開発環境)
4. [セットアップ](#セットアップ)
5. [ディレクトリ構成](#ディレクトリ構成)
6. [開発状況](#開発状況)
7. [設計資料](#設計資料)

## 概要
### プロジェクト名
IT資産管理ツール

### プロジェクトについて
小規模企業のPC・ネットワーク機器の所在・利用者・状態を把握する。

## 実装予定の機能
- 機器の情報の登録・編集・一覧・詳細表示
- キーワード検索・条件による絞り込み
- 管理番号の自動採番
- 場所・利用者・状態・種別・管理番号の変更履歴
- 機器の論理削除・復元
- 検索結果のCSV出力
- 場所・アカウントの管理
- 管理担当者・一般利用者の権限分離

## 開発環境
| 言語・フレームワーク | 記載内容 |
|----- |--------- |
| Python | 3.13.9 |
| Flask | 3.1.2 |
| MariaDB | 10.4.32 |

## セットアップ
以下のコマンドは、プロジェクトのルートフォルダーで、PowerShellを使用して実行します。
### 仮想環境の作成方法
```bash
python -m venv .venv
```
```bash
.\.venv\Scripts\python.exe --version
```
- 1行目：作品専用のPython環境を作成する。
- 2行目：作成した環境のPythonバージョンを管理する。

### 依存ライブラリのインストール方法
```bash
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
```
```bash
.\.venv\Scripts\python.exe -m pip check
```

### 環境設定ファイルの準備方法
```bash
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}
```
| 設定項目 | 設定する内容 |
|---|---|
| `SECRET_KEY` | 自分のPCで生成した秘密鍵 |
| `DB_HOST` | MariaDBの接続先 |
| `DB_PORT` | MariaDBのポート番号 |
| `DB_USER` | DB接続ユーザー名 |
| `DB_PASSWORD` | DBユーザーのパスワード |
| `DB_NAME` | 使用するDB名。現在の初期案は `it_asset_management` |
| `DB_CHARSET` | `utf8mb4` |
| `DB_COLLATION` | `utf8mb4_bin` |
| `DB_TIME_ZONE` | `+09:00` |
| `SESSION_IDLE_MINUTES` | `30` |

```bash
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```
表示された値を.envのSECRET KEYに設定してください。

### MariaDBの起動・接続確認方法
```bash
.\.venv\Scripts\python.exe scripts/check_db.py
```
| 項目 | 期待する値 |
|---|---|
| サーバーバージョン | `10.4.32-MariaDB` で始まる値 |
| 接続文字コード | `utf8mb4` |
| 接続照合順序 | `utf8mb4_bin` |
| 接続タイムゾーン | `+09:00` |

### 実装後に追加する内容
| 項目 | 追記する内容 |
|---|---|
| DB初期化 | DB・テーブル・初期データを作成する方法 |
| 初期管理担当者 | 最初の管理アカウントを作成する方法 |
| アプリ起動 | 実際の起動コマンドとアクセス先URL |
| 終了方法 | アプリやDBを終了する操作 |

## ディレクトリ構成
```text
it-asset-management
    ├─app
    │  ├─repositories
    │  ├─routes
    │  ├─services
    │  ├─static
    │  └─templates
    ├─docs
    ├─scripts
    └─sql
```

## 開発状況

現在は設計を終え、開発環境の準備を進めています。
アプリケーションの機能実装はこれから着手する予定です。

- [x] 要件定義
- [x] 画面設計・ワイヤーフレーム作成
- [x] DB設計
- [ ] 開発環境の準備（進行中）
- [ ] DB・テーブルの作成
- [ ] Flaskの基本構成の実装
- [ ] ログイン・アカウント管理機能の実装
- [ ] 場所管理機能の実装
- [ ] 機器管理・変更履歴機能の実装
- [ ] 検索・CSV出力機能の実装
- [ ] スマートフォン表示の調整
- [ ] 動作確認・不具合修正

## 設計資料

要件・画面構成・データベース構成は、以下の資料にまとめています。

| 資料 | 内容 |
|---|---|
| [要件定義書](docs/IT資産管理システム_要件定義書_v1.0.md) | 開発目的・機能要件・運用ルール |
| [画面設計書](docs/IT資産管理システム_画面設計書_v1.0.md) | 画面一覧・入力項目・画面遷移 |
| [ワイヤーフレーム](docs/画面ワイヤーフレーム.html) | 各画面のレイアウト |
| [DB設計書](docs/IT資産管理システム_DB設計書_v1.0.md) | テーブル定義・制約・ER図 |