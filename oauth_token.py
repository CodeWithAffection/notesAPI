from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from models import TokenDate
import asyncio
from fastapi import HTTPException, status, Depends
from config import settings


oath2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

secret_key = settings.secret_key
algorithm = settings.algorithm
access_token_expire_minutes = settings.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=access_token_expire_minutes)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def verify_access_token(token : str, credentials_exception):
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithm)
        id : str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenDate(id=id)
    except InvalidTokenError:
        raise credentials_exception

    return token_data

async def get_current_user(token : str = Depends(oath2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")
    return verify_access_token(token, credentials_exception)
