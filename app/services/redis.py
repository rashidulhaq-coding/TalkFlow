# inside app/services/redis.py

import aioredis
from app.core.config import config

JTI_EXPIRY = 3600

# Initialize Redis connection with authentication
try:
    token_blocklist = aioredis.from_url(
        f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/0",
        password=getattr(config, 'REDIS_PASSWORD', None),  # Optional password
        decode_responses=True
    )
except Exception as e:
    print(f"Error connecting to Redis: {e}")
    raise


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)
    return jti is not None
