def test_predict_requires_auth(client):
    response = client.post(
        "/predict",
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
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
