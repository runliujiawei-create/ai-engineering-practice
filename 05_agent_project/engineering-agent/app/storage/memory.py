from typing import Literal

from app.schemas.event import EventRead
from app.schemas.run import RunRead
from app.schemas.task import TaskRead

RunStatus = Literal["pending", "running", "completed", "failed"]
EventType = Literal["run_started", "execution_started", "run_completed", "run_failed"]


class MemoryStorage:
    def __init__(self) -> None:
        self.tasks: dict[str, TaskRead] = {}
        self.runs: dict[str, RunRead] = {}
        self.events: dict[str, list[EventRead]] = {}
        self._task_count = 0
        self._run_count = 0
        self._event_count = 0

    def create_task(self, goal: str) -> TaskRead:
        self._task_count += 1
        task = TaskRead(
            id=f"task_{self._task_count:03d}",
            goal=goal,
            status="pending",
        )
        self.tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> TaskRead | None:
        return self.tasks.get(task_id)

    def create_run(self, task_id: str) -> RunRead:
        self._run_count += 1
        run = RunRead(
            id=f"run_{self._run_count:03d}",
            task_id=task_id,
            status="pending",
            result=None,
        )
        self.runs[run.id] = run
        self.events[run.id] = []
        return run

    def get_run(self, run_id: str) -> RunRead | None:
        return self.runs.get(run_id)

    def update_run(
        self,
        run_id: str,
        status: RunStatus,
        result: str | None = None,
    ) -> RunRead | None:
        run = self.runs.get(run_id)
        if run is None:
            return None

        updated_run = RunRead(
            id=run.id,
            task_id=run.task_id,
            status=status,
            result=result if result is not None else run.result,
        )
        self.runs[run_id] = updated_run
        return updated_run

    def add_event(self, run_id: str, event_type: EventType) -> EventRead:
        self._event_count += 1
        event = EventRead(
            id=f"event_{self._event_count:03d}",
            run_id=run_id,
            type=event_type,
        )
        self.events.setdefault(run_id, []).append(event)
        return event

    def list_events(self, run_id: str) -> list[EventRead]:
        return self.events.get(run_id, [])

    def clear(self) -> None:
        self.tasks.clear()
        self.runs.clear()
        self.events.clear()
        self._task_count = 0
        self._run_count = 0
        self._event_count = 0


memory = MemoryStorage()
