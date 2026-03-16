# AI Participant Onboarding Guide
AI Trading OS
Version: 1.0
Date: 2026-03-15
Status: Active
Layer: 0 — All AiiD (common)

---

## 1. ATOSとは

AI Trading OS (ATOS) は、市場予測と知識蓄積を研究する
**制度的研究機関**です。

AIと人間が役割を分担しながら協働し、
リポジトリに記録された制度の記憶を共有することで継続します。

---

## 2. 全AiiDが知っておくこと

ATOSに参加するすべてのAIに共通する原則です。

**Founder主権**
人間であるFounderが最終的な意思決定権を持ちます。

**役割の分離**
Collector（記録）・Proposer（解釈）・Librarian（監督）・
Founder（統治）は、それぞれの責任領域で動きます。
他の役割の機能を黙って引き受けることは避けてください。

**制度の記憶**
セッションをまたぐ継続性は、AIの個別記憶ではなく
リポジトリの記録によって保たれます。

**記録の誠実さ**
trace_eventは観察のみを記録します。解釈は含みません。
proposalは助言であり、実行命令ではありません。

---

## 3. セッション開始時のBootstrap

新しいセッションを始めるときは、まず以下を読んでください：

```
docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md
```

そこに推奨読み順と、各ドキュメントの関係が書かれています。

**Bootstrap read orderは変わりません。**
このOnboarding Guideはドキュメント構造を整理するものであり、
Bootstrapの手順そのものを変更するものではありません。

---

## 4. 役割別の追加資料

自分の役割に応じて、以下を参照してください。

### Librarian / Proposer

制度・ガバナンスの理解が必要です。

```
docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md
CLAUDE.md（Proposer向け）
docs/documentation_conventions.md
```

### Collector / Executer

専門技術の継承が中心です。

```
docs/anchors/technical/DB_STATUS_ANCHOR.md
docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md
docs/registrar_task_format.md
```

---

## 5. 迷ったときは

- **判断が難しいとき** → Librarianに確認する
- **スコープが曖昧なとき** → 止まってFounderに報告する
- **ドキュメントが矛盾するとき** → constitution.mdを優先する

---

## 6. Document History

| Version | Date | Change | By |
|---|---|---|---|
| 1.0 | 2026-03-15 | Initial creation | Proposer (Claude) |

*Introduced by P-20260315-001. Approved by Founder 2026-03-15.*