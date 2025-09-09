from fastapi import APIRouter
from app.services.chat_service import ChatService
from app.services.db import get_session
from app.schemas.chat_schemas import SessionCreate,SessionResponse,SessionUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi import HTTPException, status
from uuid import UUID

router = APIRouter()
chat_service = ChatService()

@router.post("/chat")
async def chat(db_session:AsyncSession=Depends(get_session)):
    return {"message": "Hello from talkflow!"}

@router.post("/create-session", status_code=status.HTTP_201_CREATED, response_model=SessionResponse, description="Session created successfully")
async def create_session(session_create:SessionCreate, db_session:AsyncSession=Depends(get_session)):
    session = await chat_service.create_session(session_create, db_session)
    return session

@router.get("/get-session/{session_id}", response_model=SessionResponse, status_code=status.HTTP_200_OK, description="Session fetched successfully")
async def get_chat_session(session_id:UUID, db_session:AsyncSession=Depends(get_session)):
    session = await chat_service.get_chat_session(session_id, db_session)
    return session

@router.get("/get-all-sessions", response_model=list[SessionResponse], status_code=status.HTTP_200_OK, description="Sessions fetched successfully")
async def get_all_chat_sessions(user_id:UUID, db_session:AsyncSession=Depends(get_session)):
    sessions = await chat_service.get_all_chat_sessions(user_id, db_session)
    return sessions

@router.put("/update-session/{session_id}", response_model=SessionResponse, status_code=status.HTTP_200_OK, description="Session updated successfully")
async def update_session(session_id:UUID, session_update:SessionUpdate, db_session:AsyncSession=Depends(get_session)):
    session = await chat_service.update_chat_session(session_id, session_update, db_session)
    return session

@router.delete("/delete-session/{session_id}", status_code=status.HTTP_204_NO_CONTENT, description="Session deleted successfully")
async def delete_session(session_id:UUID, db_session:AsyncSession=Depends(get_session)):
    await chat_service.delete_chat_session(session_id, db_session)
    return {"message": "Session deleted successfully"}
