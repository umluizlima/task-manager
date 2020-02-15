from fastapi import FastAPI

TASKS = []

app = FastAPI()


@app.get("/tasks")
def list():
    return TASKS
