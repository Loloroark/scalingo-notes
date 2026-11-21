from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Note
from app.schemas import NoteCreate, NoteOut

app = FastAPI(title="Notes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/notes", response_model=list[NoteOut])
def list_notes(db: Session = Depends(get_db)):
    return db.scalars(select(Note).order_by(Note.id)).all()


@app.post("/notes", response_model=NoteOut, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    note = Note(content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note
