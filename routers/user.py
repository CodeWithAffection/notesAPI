from fastapi import FastAPI, HTTPException,status,Query, APIRouter
from database import SessionDep, create_db_and_tables, engine, get_db
from typing import Annotated
from sqlmodel import select, Field, SQLModel, update
from contextlib import asynccontextmanager
from models import User, UserCreate, UserGet
import utils

@asynccontextmanager
async def lifespan(router):
    create_db_and_tables()
    yield

router = APIRouter(lifespan=lifespan,
                   prefix="/users",
                   tags = ["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserGet)
def create_user(user : UserCreate, session : SessionDep):

    #hash password:
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get("/{id}/", status_code=status.HTTP_200_OK, response_model=UserGet)
def get_user(id : int, session : SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException("There is no user with this id", status_code=status.HTTP_204_NO_CONTENT)
    return user
