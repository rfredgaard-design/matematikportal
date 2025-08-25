from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from database import SessionLocal            # <-- ingen punktum
from models import Question                  # <-- ingen punktum

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("")
def list_questions(assignment_id: int, opgave_nr: int):
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
