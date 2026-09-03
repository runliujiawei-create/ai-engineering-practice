from fastapi.testclient import TestClient


def test_create_task(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"goal": "Investigate why the tests are failing"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": "task_001",
        "goal": "Investigate why the tests are failing",
        "status": "pending",
    }


def test_get_task(client: TestClient) -> None:
    created = client.post("/tasks", json={"goal": "Ship M0"}).json()

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_missing_task_returns_404(client: TestClient) -> None:
    response = client.get("/tasks/missing")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
