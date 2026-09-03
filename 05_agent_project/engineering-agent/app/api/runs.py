from fastapi import APIRouter, HTTPException

from app.schemas.event import EventRead
from app.schemas.run import RunRead
from app.storage.memory import memory

router = APIRouter()


@router.get("/runs/{run_id}", response_model=RunRead)
def get_run(run_id: str) -> RunRead:
    run = memory.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.get("/runs/{run_id}/events", response_model=list[EventRead])
def get_run_events(run_id: str) -> list[EventRead]:
    run = memory.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return memory.list_events(run_id)
