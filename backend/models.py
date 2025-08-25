from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float, JSON
from datetime import datetime
from database import Base   # <-- ingen punktum

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    images = Column(JSON, default={})
    layout = Column(JSON, default={})

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    question_number = Column(String, index=True)
    type = Column(String)
    prompt = Column(Text)
    options = Column(JSON)
    correct_answer = Column(Text)
    points = Column(Float, default=1)
