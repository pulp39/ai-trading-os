# AI Participant Onboarding Guide
AI Trading OS
Version: 1.2
Date: 2026-03-15
Status: Active
Layer: 0 — All AiiD (common)

---

## Bootstrap（最初に読んでください / Read First）

このドキュメントを読む前に、まず以下で制度状態を再構築することを
お勧めします：

```
docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md
```

Before reading this document, AI participants are encouraged to
reconstruct the institutional state using the bootstrap anchor:

```
docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md
```

The bootstrap anchor defines the reading order required to reconstruct
the current institutional state. This onboarding guide provides
role-specific context after that reconstruction.

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

新しいセッションを始めるときは、まず以下の順に読んでください。

```
1. docs/anchors/ATOS_BOOTSTRAP_ANCHOR.md
2. docs/ai_participant_onboarding.md（このファイル）
```

ATOS_BOOTSTRAP_ANCHOR.md に推奨読み順と、
各ドキュメントの関係が書かれています。

**Bootstrap read orderは変わりません。**
このOnboarding Guideはドキュメント構造を整理するものであり、
Bootstrapの手順そのものを変更するものではありません。

---

## 4. 役割別の最小限読み順

新しいセッションを始めるとき、役割に応じて以下を参照することを
お勧めします。Section 3 の共通手順を前提として、ここでは役割ごとの
追加資料のみを示します。

---

### Librarian

- `constitution.md`
- `docs/amendments/FR-20260312-003.md`
- `docs/amendments/FR-20260312-004.md`
- `docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md`
- `docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md`
- `docs/aiid_registry.md`
- `docs/BOUNDARY.md`
- `docs/documentation_conventions.md`

---

### Proposer

- `constitution.md`
- `docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md`
- `CLAUDE.md`
- `docs/proposal_semantics.md`
- `docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md`

---

### Assistant Registrar（OpenClaw）

- `docs/anchors/governance/EXECUTION_MODEL_ANCHOR.md`
- `docs/registrar_task_format.md`
- `docs/anchors/technical/OPENCLAW_REGISTRAR_TRAINING_ANCHOR.md`
- `docs/anchors/technical/DB_STATUS_ANCHOR.md`
- `docs/openclaw_training_status.md`

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
| 1.1 | 2026-03-15 | Section 4: role-based minimal reading order added | Proposer (Claude) |
| 1.2 | 2026-03-15 | Bootstrap priority note added to document header | Proposer (Claude) |

*v1.0 introduced by P-20260315-001. Approved by Founder 2026-03-15.*
*v1.1 Librarian approval granted 2026-03-15.*
*v1.2 Bootstrap ambiguity resolution — Librarian review + Proposer confirmation 2026-03-15.*
