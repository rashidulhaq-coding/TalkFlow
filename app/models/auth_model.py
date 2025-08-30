from sqlmodel import SQLModel, Field, Column,text
import sqlalchemy.dialects.postgresql as pg
from typing import Optional
from uuid import UUID    
from datetime import datetime, timezone
from sqlalchemy.sql import func
import uuid

class Users(SQLModel, table=True):
    __tablename__="users"
    id:UUID=Field(sa_column=Column(pg.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, server_default=text("gen_random_uuid()")))
    username:str=Field(sa_column=Column(pg.VARCHAR(50), nullable=False))
    email:str=Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    password:str=Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False,server_default=func.now()))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False,server_default=func.now(), onupdate=func.now()))