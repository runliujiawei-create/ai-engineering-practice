from fastapi import FastAPI

from app.api import runs, tasks


app = FastAPI(title="engineering-agent")

app.include_router(tasks.router)
app.include_router(runs.router)
