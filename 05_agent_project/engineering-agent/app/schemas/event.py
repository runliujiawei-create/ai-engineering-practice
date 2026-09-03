from typing import Literal

from pydantic import BaseModel


class EventRead(BaseModel):
    id: str
    run_id: str
    type: Literal["run_started", "execution_started", "run_completed", "run_failed"]
