#!/usr/bin/env python3
"""CLI for running web UI E2E tests (Playwright + pytest)."""

import argparse
import subprocess
import sys


def run_e2e(suite: str, extra_args: list[str] | None = None) -> int:
    target = {
        "all": "tests/e2e/",
        "saucedemo": "tests/e2e/saucedemo/",
        "blazedemo": "tests/e2e/blazedemo/",
        "orangehrm": "tests/e2e/OrangeHRM/",
    }.get(suite, suite)

    cmd = [sys.executable, "-m", "pytest", target, "-v", "--tb=short"]
    if extra_args:
        cmd.extend(extra_args)
    return subprocess.run(cmd).returncode


def main() -> None:
    parser = argparse.ArgumentParser(description="Run web UI E2E tests")
    parser.add_argument(
        "command",
        nargs="?",
        default="e2e",
        choices=["e2e"],
        help="Test command (default: e2e)",
    )
    parser.add_argument(
        "--suite",
        default="all",
        choices=["all", "saucedemo", "blazedemo", "orangehrm"],
        help="E2E suite to run",
    )
    parser.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="Extra arguments passed to pytest (prefix with --)",
    )
    args = parser.parse_args()
    extra = [a for a in args.pytest_args if a != "--"]
    sys.exit(run_e2e(args.suite, extra or None))


if __name__ == "__main__":
    main()
