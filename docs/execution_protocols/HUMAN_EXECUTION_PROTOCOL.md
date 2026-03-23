📄 Human-in-the-loop Execution Protocol v0.2（最終版）

※そのまま使える確定版です

1. 目的

本プロトコルは、AI Trading OS における実行（execution）を
人間の意思決定と責任のもとで安全に実施するための手順を定義する。

2. 実行の定義
execution = 外部システムへの送信（external transmission）
scriptの完了ではない
READY_FOR_EXECUTIONでもない
外部API送信の瞬間に成立する
3. 役割分担
AI（OpenClaw / Assistant Registrar）
execution preparation（準備）を担当
READY_FOR_EXECUTION まで到達可能
Human（Founder）
execution authority（実行権限）を保持
外部送信を実施する唯一の主体
4. 実行フロー
Observation
→ Proposal
→ Gate（検証）
→ Authorization（承認）
→ READY_FOR_EXECUTION
→ Founder実行（external transmission）
→ Safety Lock
5. Founder実行ポイント

以下の瞬間を「実行」と定義する：

外部APIに対して注文を送信した瞬間

この瞬間に：

authorization_consumed 発火
不可逆状態へ遷移
6. 実行前チェックリスト（必須）

Founderは実行前に以下を確認する：

制度状態
 execution gate 通過済み
 authorization_granted が明示されている
注文内容
 銘柄・数量・価格を確認
 order preview を確認済み
市場条件
 市場時間内であることを確認
 （必要に応じて）off-hours override の状態を確認
技術状態
 正しい環境（.env / venv）である
 WSL_ENVIRONMENT_ANCHOR のチェックリストを確認済み
 接続先APIが正しい（本番 / 検証）
リスク
 cancel手順を把握している
 想定外時の対応を理解している
7. cancel可能範囲
実行前
完全にキャンセル可能
authorization は消費されない
実行後
cancelは「新たな操作」として扱う
元のexecutionは不可逆
8. authorization_consumed

以下で発火：

外部送信が行われた瞬間

特性：

成功 / 失敗 / 不明に関係なく発火
巻き戻し不可
再利用不可
9. post_submit_safety_lock

実行後に必ず適用：

目的
二重送信防止
誤操作防止
再実行防止
性質
自動適用（理想）
human操作に依存しない
10. trace_event 記録

最低限以下を記録：

実行前
execution_authorized
実行時
authorization_consumed
external_submission_attempted
実行後
post_submit_safety_lock_applied
異常系
execution_cancelled
execution_failed
transmission_unknown_detected
11. 禁止事項

以下は禁止：

AIによる外部送信
authorizationなしの実行
execution後の再送信（lock無視）
非記録のexecution
12. 原則
AIは実行しない
Humanだけが実行する
executionは必ず記録される
executionは不可逆である
13. 将来拡張性

このプロトコルは、将来の条件付き委任（delegation）や
限定的な自動化（bounded automation）が制度化された際に
拡張されることを想定している。

ただし現時点では：

Founderのみが execution authority を持つ
