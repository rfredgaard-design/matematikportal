# backend/routers/questions.py
from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("")
def list_questions(assignment_id: int = Query(...), opgave_nr: int = Query(...)):
    """
    Returnerer alle spørgsmål for en given assignment og opgavenummer (fx opgave 1 → "1.x").
    """
    prefix = f"{opgave_nr}."
    db: Session = SessionLocal()
    try:
        qs = (
            db.query(Question)
            .filter(Question.assignment_id == assignment_id)
            .filter(Question.question_number.like(f"{prefix}%"))
            .order_by(Question.question_number.asc())
            .all()
        )
        return [
            {
                "question_number": q.question_number,
                "type": q.type,
                "prompt": q.prompt,
                "options": q.options,
                "points": q.points,
            }
            for q in qs
        ]
    finally:
        db.close()




