from typing import Literal

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    goal: str = Field(min_length=1)


class TaskRead(BaseModel):
    id: str
    goal: str
    status: Literal["pending"]
