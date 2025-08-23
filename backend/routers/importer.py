# backend/routers/importer.py
from fastapi import APIRouter, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Assignment, Question
import json

router = APIRouter(prefix="/import", tags=["import"])

@router.post("/assignment")
def import_assignment(
    title: str = Form(...),
    questions_json: UploadFile = File(...),
    images_dir: str = Form("/static")  # bruges kun som info; billeder serveres typisk fra frontend
):
    """
    Importerer spørgsmål fra din questions.json og opretter et Assignment.
    Mapper opgave-nr til /static/opgave_01.png ... /static/opgave_20.png (justér efter behov).
    """
    db: Session = SessionLocal()
    try:
        qdata = json.loads(questions_json.file.read().decode("utf-8"))
        a = Assignment(title=title, description="Importerede FP9-opgaver")
        db.add(a); db.commit(); db.refresh(a)

        # Map opgave -> billedsti (kan pege på din frontend CDN, hvis du vil)
        images_map = {str(i): f"/static/opgave_{i:02d}.png" for i in range(1, 21)}
        a.images = images_map
        db.add(a); db.commit(); db.refresh(a)

        # Opret Question-poster
        for opgave in qdata:                # forventet struktur: [{ "opgave":"1", "questions":[...] }, ...]
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
