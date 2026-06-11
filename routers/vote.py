from fastapi import FastAPI, HTTPException,status,Query, APIRouter, Depends
from database import create_db_and_tables, engine, get_db
from models import Vote, User, Vote_model
import asyncio
from oauth_token import get_current_user
from sqlalchemy.orm import Session


router = APIRouter(prefix="/vote", tags=["Voting"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_vote(vote : Vote_model, session : Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    vote_query = session.query(Vote).filter(Vote.user_id == current_user.id, Vote.note_id == vote.note_id)

    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code = status.HTTP_204_NO_CONTENT)
        new_vote = Vote(user_id = current_user.id, note_id = vote.note_id)
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote)
        return {"detail" : "Vote was added"}
    else:
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
        vote_query.delete(synchronize_session = False)
        session.commit()
        return {"detail" : "Vote was deleted"}



