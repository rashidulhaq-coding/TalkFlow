from pydantic import BaseModel


class SessionCreate(BaseModel):
    name:str
    user_id:uuid.UUID

class SessionUpdate(BaseModel):
    name:str
    user_id:uuid.UUID

class SessionResponse(BaseModel):
    id:uuid.UUID
    name:str
    user_id:uuid.UUID
    created_at:datetime
    updated_at:datetime

