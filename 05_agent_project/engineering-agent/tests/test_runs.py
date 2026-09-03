from fastapi.testclient import TestClient


def test_create_run(client: TestClient) -> None:
    task = client.post("/tasks", json={"goal": "Investigate failures"}).json()

    response = client.post(f"/tasks/{task['id']}/runs")

    assert response.status_code == 200
    assert response.json()["id"] == "run_001"
    assert response.json()["task_id"] == task["id"]


def test_dummy_executor_completes_run(client: TestClient) -> None:
    task = client.post("/tasks", json={"goal": "Investigate failures"}).json()

    created_run = client.post(f"/tasks/{task['id']}/runs").json()
    response = client.get(f"/runs/{created_run['id']}")

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["result"] == "Processed: Investigate failures"


def test_get_run_events(client: TestClient) -> None:
    task = client.post("/tasks", json={"goal": "Investigate failures"}).json()
    run = client.post(f"/tasks/{task['id']}/runs").json()

    response = client.get(f"/runs/{run['id']}/events")

    assert response.status_code == 200
    assert [event["type"] for event in response.json()] == [
        "run_started",
        "execution_started",
        "run_completed",
    ]


def test_create_run_for_missing_task_returns_404(client: TestClient) -> None:
    response = client.post("/tasks/missing/runs")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_get_missing_run_returns_404(client: TestClient) -> None:
    response = client.get("/runs/missing")

    assert response.status_code == 404
    assert response.json()["detail"] == "Run not found"
