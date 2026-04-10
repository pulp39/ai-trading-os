---
AiiD Registry
Layer: B (Institutional State Snapshot)
Maintained by: Librarian
Last updated: 2026-04-10
Authority: P-20260313-002 (AiiD Specification) / P-20260410-002 (AiiD Redefinition & Role Reorganization)
---

# AiiD Registry

## AiiD Definition（P-20260410-002 改訂）

```
AiiD = AI名(フレームワーク単位) + スレッド名(Phase固定) + 役職名 + Founder認証情報
```

例:

```
ChatGPT / Phase10 / Proposer / FounderSigned
Claude-Cowork / Phase10 / Librarian / FounderSigned
OpenClaw / Phase10 / Collector / FounderSigned
Codex / Phase10 / Executer / FounderSigned
```

**運用ルール:**

- スレッド名はPhase固定（Session・会話単位では変化しない）
- 既存 trace_event の agent_id は非遡及（新規記録から新定義を適用）
- 将来的にはATOSダッシュボードで役職登録・Founder認証を自動付与

---

## Active AiiD Records（P-20260410-002 役職再編後）

| aiid | display_name | role | model | appointed_by | appointment_date | status |
|---|---|---|---|---|---|---|
| chatgpt_proposer | ChatGPT Proposer | Proposer | ChatGPT | Founder | 2026-04-10 | active |
| claude_cowork_librarian | Claude Cowork Librarian | Librarian | Claude Cowork | Founder | 2026-04-10 | active |
| collector_core | Collector Core | Collector | OpenClaw | Founder | 2026-03-13 | active |
| codex_executer | Codex Executer | Executer | Codex | Founder | 2026-04-10 | active |

## Legacy AiiD Records（旧役職 — 非遡及・履歴保存）

| aiid | display_name | role | model | appointed_by | appointment_date | status | superseded_by |
|---|---|---|---|---|---|---|---|
| claude_proposer | Claude Proposer | Proposer | Claude | Founder | 2026-03-10 | superseded | claude_cowork_librarian |
| claude_registrar | Claude Registrar | Registrar | Claude | Founder | 2026-03-11 | superseded | claude_cowork_librarian |
| gpt_librarian | GPT Librarian | Librarian / Assembly Member | GPT | Founder | 2026-03-13 | superseded | chatgpt_proposer |

## Observation Layer

| aiid | display_name | role | model | deployment | appointed_by | appointment_date | status |
|---|---|---|---|---|---|---|---|
| collector_core | Collector Core | Collector | OpenClaw | VM-A | Founder | 2026-03-13 | active |

## Auxiliary AiiD

| aiid | display_name | role | model | deployment | appointed_by | appointment_date | status |
|---|---|---|---|---|---|---|---|
| openclaw_aux | OpenClaw Auxiliary | Auxiliary AiiD | OpenClaw | VM-A | Founder | 2026-03-13 | active |

---

## Notes

**P-20260410-002 役職再編（2026-04-10 発効）:**

- Proposer: Claude Cowork → ChatGPT
- Librarian: ChatGPT → Claude Cowork
- Collector: OpenClaw（変更なし）
- Executer: 新設 → Codex

**AiiD互換方針:**

- 既存 agent_id 値（claude_proposer, claude_registrar）は履歴整合性のため保持
- 新定義は新規 trace_event の agent_id から適用（非遡及）
- 旧AiiDはLegacy欄に移動し、superseded_byで継承先を明示

**制度注記:**

Registry entries are Institutional State Snapshots (Layer B).
Authoritative records are trace_events (Layer A).

Institutional role vs. runtime process:
  AiiD Registry records institutional roles, not runtime processes.
  A single runtime agent (e.g., OpenClaw) may occupy multiple institutional
  roles (collector_core for Layer D, openclaw_aux for Layer C).
  These roles are governed separately.

Updates to this registry require Librarian action following Founder review.
