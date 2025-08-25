# backend/routers/layout.py
from fastapi import APIRouter, Body
from sqlalchemy.orm import Session

# virker både som pakke ("from ..database") og mappe ("from database")
try:
    from ..database import SessionLocal
    from ..models import Assignment
except ImportError:  # fallback hvis rootDir=backend
    from database import SessionLocal
    from models import Assignment

router = APIRouter(prefix="/layout", tags=["layout"])

@router.get("/{assignment_id}")
def get_layout(assignment_id: int):
    db: Session = SessionLocal()
    try:
        a = db.query(Assignment).get(assignment_id)
        if not a:
            return {"error": "Assignment not found"}
        return {"images": a.images, "layout": a.layout, "title": a.title}
    finally:
        db.close()

@router.put("/{assignment_id}")
def save_layout(assignment_id: int, payload: dict = Body(...)):
    """
    payload: { "layout": { "1.1": [{ "x":..,"y":..,"w":..,"h":.. }], ... } }
    """
    db: Session = SessionLocal()
    try:
        a = db.query(Assignment).get(assignment_id)
        if not a:
            return {"ok": False, "error": "Assignment not found"}
        a.layout = payload.get("layout", {})
        db.add(a); db.commit()
        return {"ok": True}
    finally:
        db.close()
from fastapi import APIRouter, Body, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Assignment, Question

router = APIRouter(prefix="/layout", tags=["layout"])

# ... eksisterende GET/PUT endpoints ...

@router.post("/{assignment_id}/autogen")
def autogen_layout(
    assignment_id: int,
    opgave_nr: int = Query(..., ge=1, le=99),
    start_x: int = Query(40),
    start_y: int = Query(80),
    width: int = Query(300),
    height: int = Query(40),
    gap: int = Query(50),
):
    """
    Opretter et standard-rect for hver question_number i den angivne opgave (fx opgave_nr=1 → '1.x').
    Felterne placeres i en lodret liste med (start_x, start_y), 'height' og 'gap' mellem felter.
    """
    db: Session = SessionLocal()
    try:
        a = db.query(Assignment).get(assignment_id)
        if not a:
            return {"ok": False, "error": "Assignment not found"}

        # find spørgsmål for denne opgave
        prefix = f"{opgave_nr}."
        qs = (
            db.query(Question)
            .filter(Question.assignment_id == assignment_id)
            .filter(Question.question_number.like(f"{prefix}%"))
            .order_by(Question.question_number.asc())
            .all()
        )

        if not qs:
            return {"ok": False, "error": f"No questions found for opgave {opgave_nr}"}

        layout = a.layout or {}
        y = start_y
        for q in qs:
            # hvis der allerede findes felter til qn, beholder vi dem (idempotent)
            if layout.get(q.question_number):
                continue
            layout[q.question_number] = [{
                "x": start_x,
                "y": y,
                "w": width,
                "h": height,
                "type": q.type or "text"
            }]
            y += height + gap

        a.layout = layout
        db.add(a); db.commit()
        return {"ok": True, "updated_layout_keys": [q.question_number for q in qs]}
    finally:
        db.close()







