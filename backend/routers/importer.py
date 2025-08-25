from fastapi import APIRouter, UploadFile, File, Form
from sqlalchemy.orm import Session
import json

from database import SessionLocal             # <-- ingen punktum
from models import Assignment, Question       # <-- ingen punktum

router = APIRouter(prefix="/import", tags=["import"])

@router.post("/assignment")
def import_assignment(
    title: str = Form(...),
    questions_json: UploadFile = File(...),
    images_dir: str = Form("/static")
):
    db: Session = SessionLocal()
    try:
        qdata = json.loads(questions_json.file.read().decode("utf-8"))
        a = Assignment(title=title, description="Importerede FP9-opgaver")
        db.add(a); db.commit(); db.refresh(a)

        images_map = {str(i): f"/static/opgave_{i:02d}.png" for i in range(1, 21)}
        a.images = images_map
        db.add(a); db.commit(); db.refresh(a)

        for opgave in qdata:
            for q in opgave.get("questions", []):
                db.add(Question(
                    assignment_id=a.id,
                    question_number=q.get("question_number"),
                    type=q.get("type", "text"),
                    prompt=q.get("prompt", ""),
                    options=q.get("options", []),
                    correct_answer=(q.get("correct_answer") or ""),
                    points=float(q.get("points", 1))
                ))
        db.commit()
        return {"assignment_id": a.id, "images": a.images, "title": a.title}
    finally:
        db.close()
