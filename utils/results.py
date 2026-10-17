"""Persist lightweight test-run summaries as JSON."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY_PATH = ROOT / "reports" / "run_history.json"
HISTORY_PATH.parent.mkdir(exist_ok=True)

def record_run(exit_code, duration_seconds, passed=None, failed=None, errors=None, total=None):
    record = {
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "exit_code": int(exit_code),
        "duration_seconds": round(float(duration_seconds), 2),
        "passed": int(passed or 0),
        "failed": int(failed or 0),
        "errors": int(errors or 0),
        "total": int(total or 0),
    }
    if HISTORY_PATH.exists():
        try:
            history = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            history = []
    else:
        history = []
    history.append(record)
    HISTORY_PATH.write_text(json.dumps(history, indent=2), encoding="utf-8")
    return record
