from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    REFRESH_TOKEN_EXPIRE_MINUTES:int
    REDIS_HOST:str
    REDIS_PORT:int
    REDIS_PASSWORD:str

    model_config=SettingsConfigDict(
        env_file=".env",
         extra="ignore"
    )

config = Settings()