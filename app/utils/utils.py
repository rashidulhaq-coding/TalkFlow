from passlib.context import CryptContext
from datetime import timedelta,datetime
import jwt
import uuid
from app.core.config import config
from fastapi import HTTPException, status

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_data:dict, expiry:timedelta=None, refresh:bool=False)-> str:
    if expiry is None:
        expiry = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    paload={
        'user':user_data,
        'exp':datetime.now()+expiry,
        'jti':str(uuid.uuid4()),
        'refresh':refresh
    }
    return jwt.encode(paload,SECRET_KEY,algorithm=ALGORITHM)

def decode_access_token(token:str)-> dict:
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")