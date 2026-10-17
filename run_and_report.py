"""Run pytest, save a run summary, and rebuild the HTML dashboard."""
import subprocess
import sys
import time
from pathlib import Path
from utils.results import record_run, ROOT

start = time.perf_counter()
result = subprocess.run([sys.executable, "-m", "pytest", "-v"], cwd=ROOT)
duration = time.perf_counter() - start

# Pytest's terminal summary is not a stable machine-readable API, so run again
# with a JUnit XML output and parse that result for reliable counts.
xml_path = ROOT / "reports" / "last_run.xml"
xml_result = subprocess.run(
    [sys.executable, "-m", "pytest", "-q", f"--junitxml={xml_path}"],
    cwd=ROOT,
)
try:
    import xml.etree.ElementTree as ET
    root = ET.parse(xml_path).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    total = int(suite.attrib.get("tests", 0)) if suite is not None else 0
    failures = int(suite.attrib.get("failures", 0)) if suite is not None else 0
    errors = int(suite.attrib.get("errors", 0)) if suite is not None else 0
    skipped = int(suite.attrib.get("skipped", 0)) if suite is not None else 0
    passed = max(0, total - failures - errors - skipped)
except Exception:
    total, failures, errors, passed = 0, 0, 0, 0

record_run(xml_result.returncode, duration, passed, failures, errors, total)
subprocess.run([sys.executable, str(ROOT / "reports" / "build_dashboard.py")], cwd=ROOT)
sys.exit(xml_result.returncode)
