from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth_schemas import UserCreate, UserUpdate, UserResponse
from app.services.db import get_session
from app.services.user_service import UserService
from uuid import UUID
from app.utils.utils import get_password_hash

auth_router=APIRouter(tags=["Authentication"])
user_service=UserService()

@auth_router.post("/create-user",status_code=status.HTTP_201_CREATED,response_model=UserResponse, description="User created successfully")
async def create_user(user_data:UserCreate, db_session:AsyncSession=Depends(get_session)):
    user=await user_service.create_user(user_data,db_session)
    return user

@auth_router.get("/get-user/{user_email}",response_model=UserResponse, status_code=status.HTTP_200_OK, description="User fetched successfully")
async def get_user(user_email:str, db_session:AsyncSession=Depends(get_session)):
    user=await user_service.get_user(user_email,db_session)
    return user

@auth_router.get("/get-all-users",response_model=list[UserResponse], status_code=status.HTTP_200_OK, description="Users fetched successfully")
async def get_all_users(db_session:AsyncSession=Depends(get_session)):
    users=await user_service.get_all_users(db_session)
    return users

@auth_router.put("/update-user/{user_email}",response_model=UserResponse, status_code=status.HTTP_200_OK, description="User updated successfully")
async def update_user(user_email:str,user_data:UserUpdate,db_session:AsyncSession=Depends(get_session)):
    user=await user_service.update_user(user_email,user_data,db_session)
    return user

@auth_router.delete("/delete-user/{user_email}",status_code=status.HTTP_204_NO_CONTENT, description="User deleted successfully")
async def delete_user(user_email:str,db_session:AsyncSession=Depends(get_session)):
    await user_service.delete_user(user_email,db_session)
    return {"message": "User deleted successfully"}
