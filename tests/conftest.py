"""Shared pytest fixtures and session metrics export for reporting."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pytest
from playwright.sync_api import Page

from automation_testing_playground.pages.saucedemo_pages.cart_page import CartPage
from automation_testing_playground.pages.saucedemo_pages.login_page import LoginPage

REQ_ID_PATTERN = re.compile(r"\b(SDC|BZD|OHR)-[A-Z]+-\d{3}\b")
METRICS_PATH = Path(__file__).resolve().parents[1] / "reports" / "metrics-latest.json"
EXECUTIONS_PATH = Path(__file__).resolve().parents[1] / "reports" / "test-executions.json"


def _suite_from_nodeid(nodeid: str) -> str:
    lower = nodeid.lower()
    if "saucedemo" in lower:
        return "SauceDemo"
    if "blazedemo" in lower:
        return "BlazeDemo"
    if "orangehrm" in lower:
        return "OrangeHRM"
    return "Other"


def _req_id_from_item(item: pytest.Item) -> str | None:
    doc = getattr(item.obj, "__doc__", None) or ""
    match = REQ_ID_PATTERN.search(doc)
    return match.group(0) if match else None


def _normalize_status(report: pytest.TestReport) -> str:
    if getattr(report, "wasxfail", None):
        return "XFAILED"
    if report.passed:
        return "PASSED"
    if report.skipped:
        return "SKIPPED"
    if report.failed:
        return "FAILED"
    return "UNKNOWN"


@pytest.fixture
def logged_in_inventory(page: Page) -> CartPage:
    """SauceDemo session on the inventory page after successful login."""
    login = LoginPage(page)
    login.login_with_valid_credentials()
    login.assert_inventory_visible()
    return CartPage(page)


def pytest_configure(config: pytest.Config) -> None:
    config._metrics_records: list[dict] = []  # type: ignore[attr-defined]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    duration = getattr(report, "duration", 0.0) or 0.0
    status = _normalize_status(report)
    nodeid = report.nodeid
    record = {
        "nodeid": nodeid,
        "name": nodeid.split("::")[-1],
        "suite": _suite_from_nodeid(nodeid),
        "requirementId": _req_id_from_item(item),
        "status": status,
        "durationSeconds": round(float(duration), 3),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    item.config._metrics_records.append(record)  # type: ignore[attr-defined]


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    records: list[dict] = getattr(session.config, "_metrics_records", [])
    if not records:
        return

    passed = sum(1 for r in records if r["status"] == "PASSED")
    failed = sum(1 for r in records if r["status"] == "FAILED")
    skipped = sum(1 for r in records if r["status"] == "SKIPPED")
    xfailed = sum(1 for r in records if r["status"] == "XFAILED")
    total = len(records)
    pass_rate = round((passed / total) * 100, 1) if total else 0.0
    duration_total = round(sum(r["durationSeconds"] for r in records), 2)

    by_suite: dict[str, dict] = {}
    for record in records:
        suite = record["suite"]
        bucket = by_suite.setdefault(
            suite,
            {"passed": 0, "failed": 0, "skipped": 0, "xfailed": 0, "total": 0},
        )
        bucket["total"] += 1
        status = record["status"]
        if status == "PASSED":
            bucket["passed"] += 1
        elif status == "FAILED":
            bucket["failed"] += 1
        elif status == "SKIPPED":
            bucket["skipped"] += 1
        elif status == "XFAILED":
            bucket["xfailed"] += 1

    by_requirement = {
        r["requirementId"]: r["status"]
        for r in records
        if r.get("requirementId")
    }

    payload = {
        "runId": datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "exitStatus": exitstatus,
        "durationSeconds": duration_total,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "xfailed": xfailed,
            "passRate": pass_rate,
        },
        "bySuite": by_suite,
        "byRequirement": by_requirement,
        "tests": records,
    }

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    history_entry = {
        "id": payload["runId"],
        "suite": "Web UI E2E (all)",
        "status": "SUCCESS" if failed == 0 else "FAILED",
        "totalTests": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "xfailed": xfailed,
        "passRate": pass_rate,
        "duration": f"{duration_total}s",
        "timestamp": payload["timestamp"],
    }
    executions: list = []
    if EXECUTIONS_PATH.exists():
        try:
            executions = json.loads(EXECUTIONS_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            executions = []
    if not isinstance(executions, list):
        executions = []
    executions.insert(0, history_entry)
    executions = executions[:30]
    EXECUTIONS_PATH.write_text(json.dumps(executions, indent=2), encoding="utf-8")
