from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, TIMESTAMP,text
from pydantic import BaseModel, EmailStr
from sqlalchemy import ForeignKey
Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, primary_key=False, nullable=False)
    content = Column(String, primary_key = False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), primary_key=False, nullable=False, server_default=text("now()"))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class NoteCreate(BaseModel):
    title : str
    content : str

class NoteUpdate(BaseModel):
    title : str | None = None
    content : str | None = None

class NoteGet(BaseModel):
    id : int
    title : str
    content : str
    created_at : datetime
    owner_id : int


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, primary_key=False, nullable=False)
    password = Column(String, primary_key=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), primary_key=False, nullable=False, server_default=text("now()"))
    

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserGet(BaseModel):
    email : EmailStr
    id : int
    created_at : datetime

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class TokenDate(BaseModel):
    id : int | None = None  

class Vote_model(BaseModel):
    dir : int
    note_id : int

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    note_id = Column(Integer, ForeignKey("notes.id"), primary_key=True, nullable=False)

