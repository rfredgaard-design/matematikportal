# backend/routers/layout.py
from fastapi import APIRouter, Body
from sqlalchemy.orm import Session
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
