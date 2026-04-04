import os
import time

import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def wait_for_service(url: str, timeout: int = 120) -> None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return
        except requests.RequestException:
            pass
        time.sleep(3)
    raise RuntimeError(f"Service did not become ready in time: {url}")


def main() -> None:
    wait_for_service(f"{BASE_URL}/health")
    wait_for_service(f"{BASE_URL}/db-health")

    health = requests.get(f"{BASE_URL}/health", timeout=10)
    assert health.status_code == 200, health.text
    health_json = health.json()
    assert health_json["status"] == "ok"
    assert health_json["model_exists"] is True

    db_health = requests.get(f"{BASE_URL}/db-health", timeout=10)
    assert db_health.status_code == 200, db_health.text
    assert db_health.json()["status"] == "ok"

    register_response = requests.post(
        f"{BASE_URL}/register",
        json={
            "username": "ci_user",
            "password": "strongpass123",
        },
        timeout=10,
    )

    if register_response.status_code not in (201, 400):
        raise AssertionError(
            f"Unexpected register response: {register_response.status_code} {register_response.text}"
        )

    login_response = requests.post(
        f"{BASE_URL}/login",
        json={
            "username": "ci_user",
            "password": "strongpass123",
        },
        timeout=10,
    )
    assert login_response.status_code == 200, login_response.text

    token = login_response.json()["access_token"]

    predict_response = requests.post(
        f"{BASE_URL}/predict",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "crim": 0.02729,
            "zn": 0.0,
            "indus": 7.07,
            "chas": 0,
            "nox": 0.469,
            "rm": 7.185,
            "age": 61.1,
            "dis": 4.9671,
            "rad": 2,
            "tax": 242,
            "ptratio": 17.8,
            "black": 392.83,
            "lstat": 4.03,
        },
        timeout=10,
    )
    assert predict_response.status_code == 200, predict_response.text

    predict_json = predict_response.json()
    assert predict_json["stored"] is True
    assert "request_id" in predict_json
    assert "predicted_medv" in predict_json

    print("Functional scenario passed successfully.")


if __name__ == "__main__":
    main()
