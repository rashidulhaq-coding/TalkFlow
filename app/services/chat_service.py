from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat_models import Sessions
from uuid import UUID
from app.schemas.chat_schemas import SessionCreate,SessionUpdate,SessionResponse
from fastapi import HTTPException, status

from sqlalchemy.future import select
class ChatService:
    
    async def create_session(self, session_create:SessionCreate, db_session:AsyncSession) -> Sessions:
        session_data = session_create.model_dump()
        session = Sessions(**session_data)
        db_session.add(session)
        await db_session.commit()
        return session
    
    async def get_chat_session(self, session_id: UUID, db_session: AsyncSession) -> Sessions:
        stmt = select(Sessions).where(Sessions.id == session_id)
        result = await db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_chat_sessions(self, user_id: UUID, db_session:AsyncSession) -> list[Sessions]:
        stmt = select(
        Sessions.id,
        Sessions.name,
        Sessions.user_id,
        Sessions.created_at,
        Sessions.updated_at
    ).where(Sessions.user_id == user_id)
    
        result = await db_session.execute(stmt)
        sessions = result.all()
        
        return [
            SessionResponse(
                id=session.id,
                name=session.name,
                created_at=session.created_at,
                updated_at=session.updated_at
            )
            for session in sessions
        ]
    
    async def update_chat_session(self, session_id: UUID, session_update: SessionUpdate, db_session: AsyncSession) -> Sessions:
        stmt = select(Sessions).where(Sessions.id == session_id)
        result = await db_session.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        
        session_data = session_update.model_dump()
        for key, value in session_data.items():
            setattr(session, key, value)
            
        await db_session.commit()
        await db_session.refresh(session)
        return session
    
    async def delete_chat_session(self, session_id: UUID, db_session: AsyncSession) -> None:
        stmt = select(Sessions).where(Sessions.id == session_id)
        result = await db_session.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        
        await db_session.delete(session)
        await db_session.commit()
        return None