from sqlalchemy import select

from app.database import SessionLocal
from app.models import Note

with SessionLocal() as db:
    if db.scalars(select(Note)).first() is None:
        db.add_all([Note(content="Première note"), Note(content="Hello Scalingo")])
        db.commit()
        print("Seed OK")
    else:
        print("Déjà des données, rien à faire")
