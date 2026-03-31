# RUNTIME_ENVIRONMENT_ANCHOR

## Role
Runtime Layer（実行環境・復旧・トラブル統合）

---

## Purpose
WSL / PowerShell / env / venv の再現可能な実行環境を定義する

---

## Runtime Base
/mnt/c/ai-trading-os-private

---

## Standard Startup

```bash
cd /mnt/c/ai-trading-os-private
export PATH=$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0
source ./.env.local
source scripts/registrar/.venv/bin/activate
```

---

## Validation Checklist

* pwd
* which python
* which powershell.exe
* env 確認

---

## PowerShell Bridge

* powershell.exe が PATH で解決されること
* env が継承されること

---

## Common Failure

### 1. env 読み込みミス

誤: scripts/registrar/.env.local.wsl
正: ./.env.local

---

### 2. workspace drift

必ず runtime base を確認

---

### 3. venv 未有効化

python が system を向いていないか確認

---

## Recovery Procedure

1. runtime base に戻る
2. env 再source
3. venv 再activate
4. PowerShell確認

---

## Preflight Success Conditions

以下がすべて成立した場合、runtime preflight は成功とみなす：

- runtime base が `/mnt/c/ai-trading-os-private` である
- `python` が `scripts/registrar/.venv` 配下を指す
- `powershell.exe` が PATH で解決される
- `.env.local` 由来の必要環境変数が可視である

---

## Notes

本アンカーは以下を統合：

* WSL_ENVIRONMENT_ANCHOR
* OBSERVATION_PREVIEW_RUNTIME_RECOVERY_ANCHOR
* OPENCLAW_TROUBLESHOOTING_ANCHOR
