import asyncio
# from app.services.database_service import initdb
from app.utils.utils import create_access_token,decode_access_token
from app.core.config import config
from datetime import timedelta
from app.services.redis import add_jti_to_blocklist,token_in_blocklist
# asyncio.run(initdb())

async def main():
    await add_jti_to_blocklist("test")   
    print(await token_in_blocklist("test"))

asyncio.run(main())