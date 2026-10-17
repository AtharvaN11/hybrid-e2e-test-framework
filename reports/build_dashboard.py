"""Build a self-contained HTML dashboard from recorded test runs."""
import json
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "reports" / "run_history.json"
OUTPUT = ROOT / "reports" / "dashboard.html"

if HISTORY.exists():
    try:
        runs = json.loads(HISTORY.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        runs = []
else:
    runs = []

latest = runs[-1] if runs else {}
total = latest.get("total", 0)
passed = latest.get("passed", 0)
pass_rate = round((passed / total) * 100, 1) if total else 0
# A test is flagged as inconsistent if its outcome differs across stored runs.
# The demo runner records run-level counts only, so this is a run-level warning
# indicator rather than per-test historical flakiness detection.
inconsistent = sum(1 for r in runs if r.get("exit_code") != (runs[-1].get("exit_code") if runs else 0))
rows = ""
for index, run in enumerate(reversed(runs), start=1):
    rate = round(run.get("passed", 0) / run.get("total", 1) * 100, 1) if run.get("total", 0) else 0
    status = "PASS" if run.get("exit_code") == 0 else "CHECK"
    rows += (
        "<tr><td>" + escape(str(run.get("timestamp", ""))) + "</td>"
        "<td>" + status + "</td><td>" + str(run.get("passed", 0)) + "</td>"
        "<td>" + str(run.get("failed", 0)) + "</td><td>" + str(run.get("errors", 0)) + "</td>"
        "<td>" + str(run.get("duration_seconds", 0)) + " s</td><td>" + str(rate) + "%</td></tr>"
    )
if not rows:
    rows = '<tr><td colspan="7">No test runs recorded yet. Run python run_and_report.py.</td></tr>'

html = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Automation Test Health</title>
<style>
*{box-sizing:border-box}body{font-family:Arial,sans-serif;background:#f4f7fb;color:#172033;margin:0;padding:32px}
main{max-width:1100px;margin:auto}.hero{background:#123b52;color:white;padding:28px;border-radius:16px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin:20px 0}
.card{background:white;padding:20px;border-radius:12px;box-shadow:0 3px 12px #142b3b12}
.label{font-size:13px;color:#667085}.value{font-size:28px;font-weight:bold;margin-top:8px}
section{background:white;padding:20px;border-radius:12px;overflow:auto}
table{width:100%;border-collapse:collapse;min-width:650px}th,td{text-align:left;padding:12px;border-bottom:1px solid #e5e7eb}
th{font-size:12px;color:#667085;text-transform:uppercase}small{color:#667085}
</style></head><body><main><div class="hero"><h1>Automation Test Health</h1>
<p>API + browser UI + SQLite · Local demo framework</p></div>
<div class="cards">
<div class="card"><div class="label">Latest pass rate</div><div class="value">""" + str(pass_rate) + """%</div></div>
<div class="card"><div class="label">Tests in latest run</div><div class="value">""" + str(total) + """</div></div>
<div class="card"><div class="label">Latest duration</div><div class="value">""" + str(latest.get("duration_seconds", 0)) + """ s</div></div>
<div class="card"><div class="label">Recorded runs</div><div class="value">""" + str(len(runs)) + """</div></div>
</div><section><h2>Run history</h2><table><thead><tr><th>Timestamp</th><th>Status</th>
<th>Passed</th><th>Failed</th><th>Errors</th><th>Duration</th><th>Pass rate</th></tr></thead>
<tbody>""" + rows + """</tbody></table><p><small>Flakiness requires comparing individual test outcomes across repeated runs. This starter dashboard records run-level history only; it does not claim reliable per-test flaky detection.</small></p></section>
</main></body></html>"""
OUTPUT.write_text(html, encoding="utf-8")
print(f"Dashboard written to: {OUTPUT}")
