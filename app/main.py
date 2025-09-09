from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database, deps
import json
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.txt")

models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
async def root():
    return {
        "message": "Welcome to the FastAPI application! "
        "You can use this API to manage your notes."
    }
    
@app.get("/notes")
async def get_notes_file():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            lineas = file.readlines()
        notas = [{"note": linea.strip()} for linea in lineas]
        return notas
    except FileNotFoundError:
        return {"notes": [], "message": "El archivo no existe aún"}

@app.get("/notes-db", response_model=list[schemas.NoteResponse])
async def get_notes(db: Session = Depends(deps.get_db)):
    notes = db.query(models.Nota).all()
    return notes

@app.get("/conteo")
async def conteo_notas():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            lineas = file.readlines()
        return {"conteo": len(lineas)}
    except FileNotFoundError:
        return {"conteo": 0, "message": "El archivo no existe aún"}
    
@app.get("/autor")
async def get_autor():
    autor = os.getenv("AUTOR", "Autor no configurado")
    return {"autor": autor}

@app.post("/notes", response_model=schemas.NoteResponse)
async def create_note(note: schemas.NoteCreate, db: Session = Depends(deps.get_db)):
    with open(DATA_FILE, "a", encoding="utf-8") as file:
        file.write(f"{note.title} - {note.content}\n")
        
    new_note = models.Nota(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.post("/notes-file")
async def create_note_file(note: schemas.NoteCreate):
    with open(DATA_FILE, "a", encoding="utf-8") as file:
        file.write(f"{note.title} - {note.content}\n")
    return {"note": note, "message": "Note saved to file successfully!"}

    