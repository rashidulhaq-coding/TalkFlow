from pydantic import BaseModel
import uuid
from datetime import datetime


class SessionCreate(BaseModel):
    name:str
    user_id:uuid.UUID

class SessionUpdate(BaseModel):
    name:str

class SessionResponse(BaseModel):
    id:uuid.UUID
    name:str
    created_at:datetime
    updated_at:datetime

