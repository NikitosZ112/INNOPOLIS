from fastapi import FastAPI, Depends, HTTPException
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
    user_id: int

class TaskOut(BaseModel):
    id: int
    name: str
    deadline: date
    user_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks/")
def read_tasks(user_id: int, db: Session = Depends(get_db)):
    try:
        tasks = get_tasks(db, user_id)
        return [{"id": t.id, "name": t.name, "deadline": str(t.deadline)} for t in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks/")
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task.name, task.deadline, task.user_id)

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int, user_id: int, db: Session = Depends(get_db)):
    if not delete_task(db, task_id, user_id):
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return {"status": "success"}