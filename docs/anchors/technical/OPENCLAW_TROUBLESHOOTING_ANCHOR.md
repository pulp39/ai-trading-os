anchor_id: OPENCLAW_TROUBLESHOOTING_ANCHOR
title: OpenClaw Troubleshooting and Recovery Procedures
type: technical
status: active
created: 2026-03-25
author: Librarian
---

# OPENCLAW TROUBLESHOOTING ANCHOR

## Purpose

Provide deterministic recovery procedures for common OpenClaw runtime failures.

This anchor is intended to:

- minimize recovery time
- ensure reproducible fixes
- prevent repeated investigation of known issues

---

## Core Recovery Patterns

### AUTH Failure (OAuth)

Symptom:
- OAuth token refresh failed
- All models failed

Resolution:

openclaw configure --section model


---

### Gateway Failure

Symptom:
- Gateway not reachable

Resolution:

systemctl --user restart openclaw-gateway.service


---

### Node Offline

Resolution:

openclaw node run
openclaw devices approve --latest


---

## KabuStation Integration Rules

- KABU_API_HOST must be `localhost`
- KABU_API_PORT must be explicitly set (18080 production)
- Do not use `127.0.0.1`
- API interaction should occur on Windows side, not WSL

---

> ⚠️ Status: deprecated  
> This content has been consolidated into `docs/anchors/technical/RUNTIME_ENVIRONMENT_ANCHOR.md`.  
> Refer to that anchor for current runtime, recovery, and troubleshooting guidance.

---

## Environment Rules

- Always activate correct venv
- Validate python path before execution

---

## Minimal Recovery Sequence

openclaw node run
systemctl --user restart openclaw-gateway.service
openclaw configure --section model

---

## Notes

- OAuth issues cannot be resolved by restart alone
- Gateway should be managed via systemd service
- Node should be manually controlled

---

End of Anchor