from app.schemas.run import RunRead
from app.schemas.task import TaskRead
from app.storage.memory import memory


class DummyExecutor:
    def execute(self, task: TaskRead) -> str:
        return f"Processed: {task.goal}"


class RunService:
    def __init__(self, executor: DummyExecutor) -> None:
        self.executor = executor

    def create_run(self, task_id: str) -> RunRead | None:
        task = memory.get_task(task_id)
        if task is None:
            return None

        run = memory.create_run(task_id=task.id)
        memory.add_event(run_id=run.id, event_type="run_started")

        memory.update_run(run_id=run.id, status="running")
        memory.add_event(run_id=run.id, event_type="execution_started")

        try:
            result = self.executor.execute(task)
        except Exception:
            memory.update_run(run_id=run.id, status="failed")
            memory.add_event(run_id=run.id, event_type="run_failed")
            return memory.get_run(run.id)

        memory.update_run(run_id=run.id, status="completed", result=result)
        memory.add_event(run_id=run.id, event_type="run_completed")
        return memory.get_run(run.id)


run_service = RunService(executor=DummyExecutor())
