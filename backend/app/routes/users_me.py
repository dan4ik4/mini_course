from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi_users.manager import BaseUserManager
from app.models.user import User
from app.auth.deps import current_active_user, get_user_manager
from app.auth.deps import get_async_session
from pydantic import BaseModel
from typing import Optional
from fastapi_users.password import PasswordHelper
from app.schemas.user import UserRead, UserUpdateSelf

router = APIRouter(prefix="/users", tags=["users"])

password_helper = PasswordHelper()

@router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
async def read_me(user: User = Depends(current_active_user)):
    return user

class UserSelfUpdate(BaseModel):
    password: Optional[str] = None

@router.patch("/me", response_model=UserRead, summary="Update current user (self)")
async def update_me(
    data: UserUpdateSelf,
    me: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    if data.password:
        me.hashed_password = password_helper.hash(data.password)

    await session.commit()
    await session.refresh(me)
    return me
            

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_me(
    user: User = Depends(current_active_user),
    manager: BaseUserManager[User, UUID] = Depends(get_user_manager),
):
    await manager.delete(user)
    return