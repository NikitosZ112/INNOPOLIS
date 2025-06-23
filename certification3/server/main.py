from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Task
from crud import get_tasks, create_task, delete_task
from pydantic import BaseModel
from datetime import date

app = FastAPI()

# Создание таблиц
Base.metadata.create_all(bind=engine)

class TaskCreate(BaseModel):
    name: str
    deadline: str  # DD.MM.YYYY

class TaskOut(BaseModel):
    id: int
    name: str
    deadline: date

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks", response_model=list[TaskOut])
def read_tasks(db: Session = Depends(get_db)):
    tasks = get_tasks(db)
    return tasks

@app.post("/tasks", response_model=TaskOut)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = create_task(db, task.name, task.deadline)
    return new_task

@app.delete("/tasks/{task_id}", response_model=bool)
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    success = delete_task(db, task_id)
    return success