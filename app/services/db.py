from app.core.config import config
from sqlmodel import create_engine,text
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

engine = AsyncEngine(
    create_engine(config.DATABASE_URL,echo=True)
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
