from sqlmodel import SQLModel, Field, Column,text
import sqlalchemy.dialects.postgresql as pg
from typing import Optional
from sqlalchemy import ForeignKey
from uuid import UUID
from datetime import datetime
import uuid
from app.models.auth_model import Users
from sqlalchemy.sql import func

class Sessions(SQLModel, table=True):
    __tablename__="sessions"
    id:UUID=Field(sa_column=Column(pg.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, server_default=text("gen_random_uuid()")))
    name:str=Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    user_id:Users=Field(sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("users.id"), nullable=False))
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False,server_default=func.now()))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False,server_default=func.now(), onupdate=func.now()))


class Messages(SQLModel, table=True):
    __tablename__="messages"
    id: UUID=Field(sa_column=Column(pg.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, server_default=text("gen_random_uuid()")))
    session_id:Sessions=Field(sa_column=Column(pg.UUID(as_uuid=True),  ForeignKey("sessions.id"), nullable=False))
    role:str=Field(sa_column=Column(pg.VARCHAR(20), nullable=False))
    content:str=Field(sa_column=Column(pg.TEXT, nullable=False))
    message_metadata: Optional[dict] = Field(sa_column=Column(pg.JSONB, nullable=True))
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False,onupdate=func.now(),server_default=func.now()))
