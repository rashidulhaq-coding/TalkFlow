from sqlmodel import SQLModel, Field, table,Column
import sqlalchemy.dialects.postgresql as pg
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
import uuid

class Users(SQLModel, table=True):
    __tablename__="users"
    id:uuid.UUID=Field(sa_column=Column(pg.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True))
    username:str=Field(sa_column=Column(pg.VARCHAR(50), nullable=False))
    email:str=Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    password:str=Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP, nullable=False,default=datetime.now()))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP, nullable=False,default=datetime.now(), onupdate=datetime.now()))