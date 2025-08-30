from app.core.config import config
from sqlmodel import create_engine,text
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

engine = AsyncEngine(
create_engine(config.DATABASE_URL,echo=True)
)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
