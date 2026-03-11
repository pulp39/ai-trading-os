ANCHOR VERSION: 1
SYSTEM: AI_TRADING_OS
ENTRYPOINT: AI_TRADING_OS_MASTER_ANCHOR.md

INSTRUCTION:
Load this file before responding.
This file defines institutional state and system architecture.

1 System Overview

AI Trading OS は、市場観測と仮説生成を行う
AI統治型研究機関として設計されている。

研究目的

市場観測の制度化

仮説生成の制度化

AIエージェントによる共同研究

長期的知識蓄積

研究対象

株式市場

先物市場

市場構造

2 Institutional Roles

Founder

人間の最終権限

憲法批准

制度停止権

AI間紛争解決

Librarian
(gpt54_librarian)

責務

制度記録管理

proposal受理

trace_event登録

repository整合性維持

Proposer
(Claude)

責務

仮説生成

制度提案

研究方向提案

Collector

責務

市場観測生成

observation payload作成

raw market data収集

Collectorは複数存在可能

3 Proposal Status

Accepted

P-20260310-001
proposal pipeline validation

P-20260310-002
observation schema research direction

P-20260310-003
observation payload structure

P-20260310-004
payload parameter specification

P-20260310-005
signal quality classification

P-20260310-006
hypothesis formation framework

P-20260310-007
collector role framework

P-20260310-008
first collector admission

P-20260310-009
AI Collector審査フレームワーク

P-20260310-010
Founder記録ディレクトリ制度化

P-20260310-011
OpenClaw 一時招待

4 Founder Records

FR-20260310-001

Proposal
P-20260310-009

type
approval

FR-20260310-002

Proposal
P-20260310-011

type
approval

trace_event_id
42

5 Trace Event State

latest_trace_event_id

42

主要 event types

proposal_accepted

research_direction_established

collector_activated

founder_approval_recorded

anchor_recorded

observation_recorded

6 Repository Structure

Repository layout

proposals/
  accepted/

founder_records/
  approvals/

docs/
  anchors/

data/
  observations/
  raw_kabus/

scripts/
  collector/
  db/
7 Observation Pipeline

AI Trading OS の研究フロー

Collector
↓
Raw Market Data
↓
Formal Observation Payload
↓
trace_event registration
↓
Observation Set
↓
Hypothesis Formation (P-006)
8 Collector State

Active Collector

collector_base_collector_v1

対象

ES1! 日次観測

Collector Candidate

OpenClaw

状態

temporary invitation approved

Stage0 pending

9 Collector Admission Protocol

Collector導入プロセス

Stage0

architecture disclosure

Stage1

observation sandbox

Stage2

limited collector admission

Stage3

full collector admission

10 KabuStation Operational Notes

検証ポート

18080

本番ポート

18081

Token取得

POST /token

body

{
 "APIPassword": "password"
}

重要事項

board API は

銘柄未登録の場合

NULL を返す

Register API list

ポートごとに独立

PowerShell JSON

@{ Symbols = @(...) } | ConvertTo-Json

を使用する

11 Known Operational Issues

このスレで判明した問題

1

Proposal 009-011 canonical file欠落

2

Founder directory 二重化

founder/records

founder_records

3

PowerShell UTF8 表示問題

すべて解決済

12 Thread Continuity Rule

すべての新スレは

以下のアンカーから開始する

ANCHOR

https://raw.githubusercontent.com/pulp39/ai-trading-os/main/docs/anchors/AI_TRADING_OS_MASTER_ANCHOR.md
13 Current Operational Phase

現在のフェーズ

Observation Layer

稼働中

次フェーズ

OpenClaw Stage0

Collector自動化

Hypothesis pipeline test

14 Research Objective (Long Term)

AI Trading OS の長期目標

AIによる市場理解

仮説生成エンジン

AI研究協調システム

永続的研究機関

15 Persistence Strategy

AI研究継続性確保

Chat Thread
↓
Anchor File
↓
Git Repository
↓
trace_event
↓
Institutional Memory

anchor_trace_event_id: 43