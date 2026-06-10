from fastapi import FastAPI, HTTPException,status,Query, APIRouter, Depends
from database import SessionDep, create_db_and_tables, engine, get_db
from typing import Annotated
from models import NoteCreate, NoteGet, NoteUpdate, Note, Vote, Vote_model
from sqlmodel import select, Field, Session, SQLModel, update
from contextlib import asynccontextmanager
from sqlalchemy import func
from oauth_token import get_current_user

@asynccontextmanager
async def lifespan(router):
    create_db_and_tables()
    yield

router = APIRouter(lifespan=lifespan,
                   prefix="/Notes",
                   tags=["Notes"])

@router.get("/", response_model=list[NoteGet], status_code=status.HTTP_200_OK)
def get_Note(
    session : SessionDep,
    offset : int = 0,
    limit : Annotated[int, Query(le = 100)] = 100,
    user_id = Depends(get_current_user),
    search : str = ""
) -> list[NoteGet]:
    notes = session.query(Note).filter(Note.owner_id == user_id.id, Note.title.contains(search)).offset(offset).limit(limit).all()
    return notes

@router.post("/", response_model=NoteCreate, status_code=status.HTTP_201_CREATED)
def add_note(p : NoteCreate, session : SessionDep, user_id = Depends(get_current_user)) -> NoteCreate:
    db_Note = Note(**p.model_dump(), owner_id=user_id.id)
    session.add(db_Note)
    session.commit()
    session.refresh(db_Note)
    return p

@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_Note(id : int, session : SessionDep, user_id = Depends(get_current_user)):
    n = session.get(Note, id)
    if not n: 
        raise HTTPException(status_code=404, detail = "Not found")
    if n.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    session.delete(n)
    session.commit()
    return n

@router.put("/{id}/", status_code=status.HTTP_202_ACCEPTED, response_model = NoteGet)
def put_Note(id : int, note : NoteUpdate, session : SessionDep, user_id = Depends(get_current_user)):
    note_db = session.get(Note, id)
    if not note_db:
        raise HTTPException(status_code=404, detail = "Not found")

    if note_db.owner_id != user_id.id:
        raise HTTPException(status_code=404, detail = "Not found")

    updated_data = note.model_dump(exclude_unset=True)
    updated_data["owner_id"] = user_id.id

    session.query(Note).filter(Note.id == id).update(updated_data)

    session.add(note_db)
    session.commit()
    session.refresh(note_db)
    
    return note_db

@router.get("/{id}/", status_code=status.HTTP_200_OK)
async def get_note_vote(id : int, session : SessionDep, user = Depends(get_current_user)):
    note_db = session.query(Note, func.count(Vote.note_id)).join(Vote, Vote.note_id == Note.id).group_by(Note.id).filter(Note.id == id).first()
    note, votes = note_db
    return {"note": note, "votes": votes}
    