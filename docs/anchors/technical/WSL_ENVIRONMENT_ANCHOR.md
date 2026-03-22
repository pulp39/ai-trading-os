# WSL_ENVIRONMENT_ANCHOR

Version: 1.0  
Status: draft  
Purpose: Runtime environment reference for WSL / Windows execution context

---

## 0. この文書をいつ読むか

以下の場合に参照してください：

- Registrar task を実行する前
- OpenClaw として作業を開始する前
- `.env` / `.venv` / Git 状態に関するエラーが発生した時
- 新しい Windows または WSL 環境でセットアップする時

この文書は **毎回のセッションで読む必要はありません**。  
実行系・環境依存系タスクの前に参照する技術補助文書です。

---

## 1. 環境構成の基本

AI Trading OS は以下の構成で動作します：

- Windows：Git / PowerShell / エディタ
- WSL：Python / 実行環境

### リポジトリパス

```text
/mnt/c/ai-trading-os-private

WSL上ではこのパスを基準とします。

2. .env 環境の原則
必須手順
source .env.local

これを実行しない場合：

DB接続失敗
環境変数未定義
スクリプト異常終了

が発生します。

3. Python 仮想環境
有効化
source .venv/bin/activate

または：

. .venv/bin/activate

未アクティブ状態では：

psycopg 未検出
module import error

が発生します。

4. よくある失敗と対処
Python コマンド
python3

を使用すること（環境による差異回避）

パス不一致
/home/vmamako
vs
/mnt/c/ai-trading-os-private

→ 常に /mnt/c/... を基準とする

/home/vmamako パス問題

OpenClaw がデフォルトで /home/vmamako/... を試みる場合があります。
正しいパスは以下です：

/mnt/c/ai-trading-os-private
psycopg 未インストール
pip install psycopg[binary]
5. Git運用上の注意
実行前チェック
git status
dirty state の場合
git restore .

または対象ファイルのみ restore

Windows / WSL 差異
大文字小文字問題
改行コード差異
パス解釈違い

→ Git状態は必ず事前確認

6. OpenClaw 実行環境（現状）

現時点では以下を基準とします：

作業ディレクトリ：

/mnt/c/ai-trading-os-private
.env.local 読み込み済み
.venv 有効化済み

※ .openclaw/workspace は将来の設計候補であり、現時点では使用しません。

7. 実行前チェックリスト

実行前に確認：

 正しいディレクトリにいる（/mnt/c/ai-trading-os-private）
 .env.local を source 済み
 .venv が有効（python3 --version で確認）
 git status が clean
 必要な依存がインストール済み（psycopg 等）
 task file が正しいスキーマ形式である（authorized_by / actions / git キーが存在する）
8. まとめ

この文書は：

実行失敗の再発防止
環境差異の吸収
AI作業の再現性確保

を目的とする補助アンカーです。

制度的文書ではなく、実行補助文書として扱います。