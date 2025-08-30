from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.db import get_session
from app.models.chat_models import Sessions
from uuid import UUID
from app.schemas.chat_schemas import SessionCreate

class ChatService:
    
    async def create_session(self, session_create:SessionCreate, db_session:AsyncSession) -> Sessions:
        session_data = session_create.model_dump()
        session = Sessions(**session_data)
        db_session.add(session)
        await db_session.commit()
        return session
    
    def get_session(self, session_id: UUID, session:AsyncSession) -> Sessions:
        session = select(Sessions).where(Sessions.id == session_id)
        return session