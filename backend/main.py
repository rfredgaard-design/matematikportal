import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers.importer import router as importer_router
from routers.layout import router as layout_router
from routers.questions import router as questions_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")  # midlertidigt; stram til din frontend-URL senere
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN] if FRONTEND_ORIGIN != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(importer_router)
app.include_router(layout_router)
app.include_router(questions_router)

@app.get("/")
def index():
    return {"ok": True}


