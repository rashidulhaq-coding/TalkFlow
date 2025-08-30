import asyncio
from app.services.database_service import initdb
asyncio.run(initdb())