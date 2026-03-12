# Registrar Preflight Standard

Purpose:
Define the operational safety checks required before executing any Registrar task.
This prevents unintended repository commits, encoding issues, and operational errors.

Scope:
Applies to all Registrar tasks executed via:
scripts/registrar/apply_registrar_task.py

---

# 1. Task File Preparation

Rules:

- Registrar task files must be created manually in an editor.
- JSON must be saved as **UTF-8 (without BOM)**.
- Do NOT generate canonical JSON using PowerShell `Set-Content`.

Allowed method:

Editor → paste content → save as UTF-8.

Reason:

PowerShell may introduce BOM encoding which can break downstream tooling.

---

# 2. Preflight Repository Check

Before running a Registrar task, run:


git status


Requirements:

- No staged changes unrelated to the Registrar task
- No unintended working directory changes

Reason:

Registrar execution may create an automatic commit.
Staged changes may be unintentionally included.

---

# 3. Dry Run Requirement

All tasks must first be executed with dry-run.

Command:


python scripts/registrar/apply_registrar_task.py --task <task_file> --dry-run


Expected result:

- Task loads successfully
- Actions are recognized
- No execution errors

If dry-run fails:
DO NOT run the live task.

---

# 4. Execution

Run the task:


python scripts/registrar/apply_registrar_task.py --task <task_file>


Expected behavior:

- trace_event inserted if required
- files created or updated if specified
- task moved to:


registrar_queue/processed/


---

# 5. Post Execution Verification

After execution run:


git status


Confirm:

- queue file removed
- processed file present

Stage the move:


git add registrar_queue/processed/<task_file>
git add -u registrar_queue/<task_file>


---

# 6. Commit

Commit the processed task move:


git commit -m "registrar: record task <task_id>"


---

# 7. Push

Push changes:


git push origin main


---

# 8. Operational Learnings

Known operational lessons recorded in trace_event:

- Registrar auto-commit may include unrelated staged changes.
- JSON canonical files must be manually saved as UTF-8.
- Dry-run is mandatory before execution.

---

# End of Standard