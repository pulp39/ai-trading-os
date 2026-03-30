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

9. 現値取得パイプライン（Collector Execution Chain）

### Current Preferred Session-Start Path

For current Phase 5 preparation, the preferred session-start path is:

1. inspect API symbol registration state
2. if registration is empty:
   - treat as session-start-equivalent
   - execute `scripts/collector/register_symbol_once.py`
3. then execute:
   - `scripts/collector/collect_board_once.py <symbol>`

This path reflects the currently validated operational sequence for restoring
`symbol_registered` and then confirming board / current price fetchability.

---

### Role of `run_collector_once.py`

`run_collector_once.py` remains available as an orchestration script.

However, it should not be treated as the default first step when symbol
registration state is unknown or empty.

The registration-state branch must be resolved first.

### 目的

本セクションは、execution前の価格確定および観測状態の整合を取るための
公式パイプラインを定義する。

このパイプラインは execution を行うものではなく、
**execution preparation の一部としての観測確定プロセス**である。

---

### 実行スクリプト

`scripts/collector/run_collector_once.py`

このスクリプトは以下の処理を順に実行する：

1. `scripts/collector/collect_board_once.py`
   - kabuStation API を通じた board / current_price 取得

2. `scripts/collector/collector_run_writer.py`
   - `collector_run` を trace_event に記録

3. `scripts/proposer/hypothesis_trigger_once.py`
   - indicator → hypothesis 生成

4. `scripts/proposer/proposal_trigger_once.py`
   - hypothesis → proposal draft 生成

---

### 用途

- current_price の確定
- board snapshot の取得
- observation → hypothesis → proposal の連動確認
- execution前の制度状態の整合確認

---

### 実行位置づけ（重要）

このパイプラインは以下の段階に属する：


Observation → Proposal → Gate（前段）


つまり：

- executionではない
- authorizationを消費しない
- external transmissionは発生しない

---

### 市場時間に関する扱い

- スクリプトは市場時間外でも実行可能（collection自体は成立）
- ただし：


execution readiness の評価は市場時間条件に依存する


したがって：

- 価格確定（Phase 1）は時間外でも可
- execution（Phase 5）は市場時間内で実施する

---

### Phase対応（重要）

このパイプラインは、以下のテストフェーズと対応する：

- Phase 1：現値取得（current_price 確定）
- Phase 2：指値生成（limit_price 計算）
- Phase 3：AAB / task 生成準備
- Phase 4：READY_FOR_EXECUTION 到達準備

---

### Phase 5との境界


Phase 5（Human Execution）は本パイプラインの外で実施される


- Founderが external transmission を行うことで execution が成立
- 本パイプラインはそこに到達する前段までを担う

---

### 注意事項

- 既定では複数銘柄（例：7203 / 8306 / 6758）を処理する
- 特定銘柄のみの観測が必要な場合は別スクリプトを検討
- `.env / venv / Git clean` が満たされていること
- WSL_ENVIRONMENT のチェックリストに従うこと

---

### 原則


観測は制度の一部であり、executionの前提条件である


This pipeline remains an important operational path for observation consistency.

However, current session-start operation must first resolve symbol registration state,
because board / current price fetch is downstream of registration.

---

## 10. OpenClaw 起動・接続手順（安定運用版）

### 概要
OpenClaw は以下の3要素で構成される：

- Gateway（常時起動）
- Node（実行主体）
- Control UI（ブラウザ）

いずれかが欠けると正常動作しない。

### 起動手順（推奨）

#### 1. Gateway 起動（WSL）
```bash
cd /mnt/c/ai-trading-os-private
source .env.local
source .venv/bin/activate
openclaw gateway --allow-unconfigured --bind lan
※ このターミナルは閉じない

2. トークン取得（別ターミナル）
openclaw dashboard --no-open

→ #token= の後ろの値を使用

3. ブラウザ接続（Windows）
http://localhost:18789/

→ token を貼って Connect

4. Node 起動（別ターミナル）
openclaw node run
5. pairing 承認（必要時）
openclaw devices approve --latest
6. 接続確認（UI）

Nodes → Refresh

状態：

paired / connected → 正常
offline → node再起動必要
よくある問題と対処
UIに接続できない
gateway が起動していない
--bind lan が不足
WSL IP と portproxy 不一致

確認：

wsl hostname -I
netsh interface portproxy show all
token mismatch

原因：

gateway 再起動後に古い token 使用

対処：

openclaw dashboard --no-open

→ 新しい token を使用

No nodes found

原因：

node 未起動

対処：

openclaw node run
pairing required

原因：

node 未承認

対処：

openclaw devices approve --latest
paired だが offline

原因：

node ターミナル終了

対処：

openclaw node run
重要な原則
gateway と node は常時起動プロセス
token は gateway 起動ごとに更新される可能性あり
UI はあくまで操作インターフェースであり本体ではない

---

## 11. KabuStation API Access Constraints（2026-03-30）

本セクションは、WSL / OpenClaw 環境から KabuStation API に接続する際に確認された制約と、実運用上の対処方法を記録する。

### 11.1 OpenClaw (Linux VM) → KabuStation API 接続制約

以下の制約が確認された：

- Windows 側で `netsh interface portproxy` によって `0.0.0.0:18080 → 127.0.0.1:18080` を設定しても、Windows HTTP.SYS / URL ACL が外部IP（172.18.x.x）からの接続を 403 Forbidden で拒否する
- OpenClaw の内蔵HTTP機能はSSRF防止フィルタによりプライベートIPへのアクセスをブロックする可能性がある
- KabuStation API は localhost 由来以外の接続を受け付けない

### 11.2 Observation 代替手段（制度内で許容）

上記制約により直接接続が困難な場合、以下の手段が有効である：

- Founder が Windows PowerShell 上で API を直接実行する（token取得・symbol登録・board取得）
- 取得結果を Proposer / Librarian に受け渡す

この方法は以下の理由により制度的に許容される：

- WRITE を伴わない（Observationのみ）
- Execution を発生させない
- Observation実装手段の変更に過ぎない

したがって、本手段は「Observation Layer 内の実装切替」として扱う。

### 11.3 PowerShell における `curl` エイリアスの注意

PowerShell の `curl` は `Invoke-WebRequest` のエイリアスであり、curlコマンドオプション（-H 等）が使用できない。
KabuStation API への接続には以下を使用すること：

- `curl.exe`（Windows版curlバイナリ）を明示する
- または `Invoke-RestMethod` を使用する

例：

```powershell
$body = '{"APIPassword":"your_password"}'
Invoke-RestMethod -Method POST -Uri "http://localhost:18080/kabusapi/token" -ContentType "application/json" -Body $body
```

### 11.4 実務上の推奨

- 接続トラブル時はまず localhost 経由で API 応答を確認する
- 外部IP経由（WSL → Windows）に固執しない
- Observation 成立を優先し、最短経路を選択する

---
