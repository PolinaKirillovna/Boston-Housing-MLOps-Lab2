"""Declarative functional test runner for the Boston Housing API.

The whole scenario lives in scenario.json: the runner waits for the
service to become ready, registers and logs in a user, captures the JWT
returned by /login, and then exercises both the unauthorized and the
authorized /predict paths. The same runner is reused unchanged by the
CD pipeline (BASE_URL can be overridden via an environment variable).
"""

import json
import os
import sys
import time
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
SCENARIO_PATH = BASE_DIR / "scenario.json"


def _expected_statuses(expected: object) -> list[int]:
    """Normalise expected_status (int or list) into a list of ints."""
    if isinstance(expected, list):
        return expected
    return [expected]


def wait_for(base_url: str, endpoints: list[str], timeout: int = 120) -> None:
    """Poll each endpoint until it returns HTTP 200 or the timeout elapses."""
    deadline = time.time() + timeout
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        while True:
            try:
                if requests.get(url, timeout=5).status_code == 200:
                    break
            except requests.RequestException:
                pass
            if time.time() > deadline:
                raise RuntimeError(f"Service did not become ready in time: {url}")
            time.sleep(3)


def run_step(step: dict, base_url: str, context: dict) -> None:
    """Execute a single scenario step and validate its response."""
    method = step["method"].upper()
    url = f"{base_url}{step['endpoint']}"

    headers = {}
    auth_var = step.get("auth")
    if auth_var:
        token = context.get(auth_var)
        if not token:
            raise AssertionError(
                f"Step '{step['name']}': saved auth variable '{auth_var}' is empty"
            )
        headers["Authorization"] = f"Bearer {token}"

    response = requests.request(
        method=method,
        url=url,
        json=step.get("json"),
        headers=headers or None,
        timeout=30,
    )

    allowed = _expected_statuses(step["expected_status"])
    if response.status_code not in allowed:
        raise AssertionError(
            f"Step '{step['name']}' failed: expected status {allowed}, "
            f"got {response.status_code}. Body: {response.text}"
        )

    try:
        body = response.json()
    except ValueError:
        body = {}

    for key, value in step.get("expected_body_contains", {}).items():
        if body.get(key) != value:
            raise AssertionError(
                f"Step '{step['name']}' failed: expected body '{key}'={value}, "
                f"got {body.get(key)}"
            )

    for key in step.get("expected_body_keys", []):
        if key not in body:
            raise AssertionError(
                f"Step '{step['name']}' failed: missing key '{key}' in response"
            )

    for var_name, body_key in step.get("save", {}).items():
        if body_key not in body:
            raise AssertionError(
                f"Step '{step['name']}' failed: cannot save '{var_name}', "
                f"key '{body_key}' missing in response"
            )
        context[var_name] = body[body_key]

    print(f"[OK] {step['name']} -> {response.status_code}")


def run_scenario() -> None:
    """Load scenario.json and execute all steps sequentially."""
    if not SCENARIO_PATH.exists():
        raise FileNotFoundError(f"Scenario file not found: {SCENARIO_PATH}")

    scenario = json.loads(SCENARIO_PATH.read_text(encoding="utf-8"))
    base_url = os.getenv("BASE_URL", scenario["base_url"])

    wait_for(base_url, scenario.get("wait_for", []))

    context: dict = {}
    for step in scenario["steps"]:
        run_step(step, base_url, context)

    print("Scenario completed successfully.")


if __name__ == "__main__":
    try:
        run_scenario()
    except (AssertionError, RuntimeError, FileNotFoundError, requests.RequestException) as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)
