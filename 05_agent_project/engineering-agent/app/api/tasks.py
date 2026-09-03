from fastapi import APIRouter, HTTPException

from app.schemas.run import RunRead
from app.schemas.task import TaskCreate, TaskRead
from app.services.run_service import run_service
from app.storage.memory import memory

router = APIRouter()


@router.post("/tasks", response_model=TaskRead)
def create_task(payload: TaskCreate) -> TaskRead:
    return memory.create_task(goal=payload.goal)


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: str) -> TaskRead:
    task = memory.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks/{task_id}/runs", response_model=RunRead)
def create_run(task_id: str) -> RunRead:
    run = run_service.create_run(task_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return run
