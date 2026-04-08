# OpenClaw Task Results

This directory stores JSON result artifacts produced by `runner.py`.

## Properties

- One file per execution
- Immutable after write
- Includes execution metadata, stdout, stderr, and STOP detection

## Naming

```
{task_id}__{UTC_TIMESTAMP}.json
```

## Lifecycle mapping

- completed → successful execution
- aborted → STOP or failure (recorded as valid outcome)
- pending → validation-only run

## Notes

- Files in this directory are execution artifacts, not definitions.
- They correspond to the `.md` task artifacts in `scripts/openclaw/tasks/`.
