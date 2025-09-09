from pydantic import BaseModel
import uuid
from datetime import datetime

class UserCreate(BaseModel):
    username:str
    email:str
    password:str

class UserUpdate(BaseModel):
    username:str
    email:str

class UserResponse(BaseModel):
    id:uuid.UUID
    username:str
    email:str
    created_at:datetime
    updated_at:datetime