from sqlalchemy.orm import Session
from models import Task
from datetime import datetime

def get_tasks(db: Session):
    return db.query(Task).all()

def create_task(db: Session, name: str, deadline_str: str):
    deadline_date = datetime.strptime(deadline_str, "%d.%m.%Y").date()
    task = Task(name=name, deadline=deadline_date)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        if db.query(Task).count() == 0:
            # Сбрасываем последовательность, если таблица пуста
            db.execute("ALTER SEQUENCE tasks_id_seq RESTART WITH 1")
            db.commit()
        return True
    return False