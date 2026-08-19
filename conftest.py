from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

pytest_plugins = ["fixtures.api_fixtures", "fixtures.auth_fixtures"]

_results: list[dict] = []
_session_start = 0.0


def pytest_sessionstart(session):
    global _session_start
    _session_start = time.time()


def pytest_runtest_logreport(report):
    # A passing test reports setup/call/teardown; only "call" carries its real
    # outcome. A test that errors or is skipped during setup never reaches
    # "call", so that's the only other phase worth recording.
    is_result_phase = report.when == "call" or (report.when == "setup" and report.outcome != "passed")
    if not is_result_phase:
        return
    _results.append({"name": report.nodeid, "status": report.outcome, "duration": round(report.duration, 4)})


def pytest_sessionfinish(session, exitstatus):
    duration = round(time.time() - _session_start, 4)
    passed = sum(1 for r in _results if r["status"] == "passed")
    failed = sum(1 for r in _results if r["status"] == "failed")
    skipped = sum(1 for r in _results if r["status"] == "skipped")

    payload = {
        "stack": "api-testing-python",
        "platform": "api",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "total": len(_results),
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "duration_seconds": duration,
        "tests": _results,
    }

    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "results.json").write_text(json.dumps(payload, indent=2))
