from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth_schemas import UserCreate, UserUpdate, UserResponse,UserLogin,Tokens
from app.services.db import get_session
from app.services.user_service import UserService
from app.utils.utils import verify_password,create_access_token
from uuid import UUID
from app.utils.utils import get_password_hash
from datetime import timedelta, datetime
from app.core.config import config
from app.services.dependencies import AccessTokenBearer,RefreshTokenBearer
from app.services.redis import add_jti_to_blocklist

auth_router=APIRouter(tags=["Authentication"])
user_service=UserService()
access_token_bearer=AccessTokenBearer()
refresh_token_bearer=RefreshTokenBearer()

@auth_router.post("/create-user",status_code=status.HTTP_201_CREATED,response_model=UserResponse, description="User created successfully")
async def create_user(user_data:UserCreate, db_session:AsyncSession=Depends(get_session)):
    user=await user_service.create_user(user_data,db_session)
    return user

@auth_router.get("/get-user/{user_email}",response_model=UserResponse, status_code=status.HTTP_200_OK, description="User fetched successfully")
async def get_user(user_email:str, db_session:AsyncSession=Depends(get_session),access_token=Depends(access_token_bearer)):
    user=await user_service.get_user(user_email,db_session)
    return user


@auth_router.put("/update-user/{user_email}",response_model=UserResponse, status_code=status.HTTP_200_OK, description="User updated successfully")
async def update_user(user_email:str,user_data:UserUpdate,db_session:AsyncSession=Depends(get_session)):
    user=await user_service.update_user(user_email,user_data,db_session)
    return user

@auth_router.delete("/delete-user/{user_email}",status_code=status.HTTP_204_NO_CONTENT, description="User deleted successfully")
async def delete_user(user_email:str,db_session:AsyncSession=Depends(get_session)):
    await user_service.delete_user(user_email,db_session)
    return {"message": "User deleted successfully"}

@auth_router.post("/login",response_model=Tokens, status_code=status.HTTP_200_OK, description="User logged in successfully")
async def login(user_data:UserLogin, db_session:AsyncSession=Depends(get_session)):
    user = await user_service.get_user(user_data.email,db_session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    access_token = create_access_token(user_data.model_dump(),expiry=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES), refresh=False)
    refresh_token = create_access_token(user_data.model_dump(),expiry=timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES), refresh=True)
    return Tokens(access_token=access_token,refresh_token=refresh_token)



@auth_router.post("/refresh-token",response_model=Tokens, status_code=status.HTTP_200_OK, description="User logged in successfully")
async def refresh_token(token_details:dict=Depends(refresh_token_bearer)):
    exp = token_details["exp"]
    if exp < int(datetime.now().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
    
    access_token = create_access_token(token_details["user"],expiry=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES), refresh=False)
    return Tokens(access_token=access_token,refresh_token="")


@auth_router.post("/revoke-token",status_code=status.HTTP_204_NO_CONTENT, description="Token revoked successfully")
async def logout(token_details:dict=Depends(access_token_bearer)):
    await add_jti_to_blocklist(token_details["jti"])
    return {"message": "Token revoked successfully"}
