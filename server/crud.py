from sqlalchemy.orm import Session
from models import Task
from datetime import datetime
from fastapi import HTTPException

def get_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()

def create_task(db: Session, name: str, deadline_str: str, user_id: int):
    deadline_date = datetime.strptime(deadline_str, "%d.%m.%Y").date()
    task = Task(name=name, deadline=deadline_date, user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task:
        db.delete(task)
        db.commit()
        if db.query(Task).count() == 0:
            db.execute("ALTER SEQUENCE tasks_id_seq RESTART WITH 1")
            db.commit()
        return True
    return False

def create_task(db: Session, name: str, deadline_str: str, user_id: int):
    try:
        # Парсим дату из строки (ожидаем YYYY-MM-DD от клиента)
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        
        if deadline < today:
            raise ValueError("Дата не может быть в прошлом")
            
        task = Task(name=name, deadline=deadline, user_id=user_id)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
        
    except ValueError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка даты: {str(e)}. Требуется формат YYYY-MM-DD"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )