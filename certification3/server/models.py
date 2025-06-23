from sqlalchemy import Column, Integer, String, Date
from database import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    deadline = Column(Date, index=True)