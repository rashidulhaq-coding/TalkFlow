from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.auth_model import Users
from uuid import UUID
from app.schemas.auth_schemas import UserCreate,UserUpdate
from fastapi import HTTPException, status
from app.utils.utils import get_password_hash

class UserService:
    
    async def create_user(self, user_create:UserCreate, db_session:AsyncSession) -> Users:
        user_data = user_create.model_dump()
        user_data["password"] = get_password_hash(user_data["password"])
        user = Users(**user_data)
        db_session.add(user)
        await db_session.commit()
        return user
    
    async def get_user(self, email: str, session:AsyncSession) -> Users:
        user = select(Users).where(Users.email == email)
        result = await session.exec(user)
        return result.first()
    
    async def check_user_exists(self, email: str, session:AsyncSession) -> bool:
        user = self.get_user(email, session)
        return True if user is not None else False
    
    async def get_all_users(self, session:AsyncSession) -> list[Users]:
        users = select(Users)
        result = await session.exec(users)
        return result.all()
    
    async def update_user(self, email: str, user_update: UserUpdate, session:AsyncSession) -> Users:
        user = self.get_user(email, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        user_data = user_update.model_dump()
        for key, value in user_data.items():
            setattr(user, key, value)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def delete_user(self, email: str, session:AsyncSession) -> None:
        user = self.get_user(email, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await session.delete(user)
        await session.commit()
        return None
    