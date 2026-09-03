from typing import Literal

from pydantic import BaseModel


class RunRead(BaseModel):
    id: str
    task_id: str
    status: Literal["pending", "running", "completed", "failed"]
    result: str | None = None
