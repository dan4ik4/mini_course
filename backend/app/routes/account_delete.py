from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi_users.manager import BaseUserManager
from app.core.db import get_db
from app.models.user import User, UserRole
from app.auth.deps import current_active_user, get_user_manager, UserRead, UserUpdate
from sqlalchemy import select
from app.auth.deps import get_async_session
from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi_users.password import PasswordHelper

router = APIRouter(prefix="/users", tags=["users"])

password_helper = PasswordHelper()

@router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
async def read_me(user: User = Depends(current_active_user)):
    return user

class UserSelfUpdate(BaseModel):
    #email: Optional[EmailStr] = None
    password: Optional[str] = None

@router.patch("/me", response_model=UserRead, summary="Update current user (self)")
async def update_me(
    data: UserSelfUpdate,
    me: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    # 1) смена email с проверкой уникальности
    # if data.email is not None and data.email != me.email:
    #     exists = await session.execute(
    #         select(User.id).where(User.email == data.email, User.id != me.id)
    #     )
    #     if exists.scalar_one_or_none():
    #         raise HTTPException(status_code=409, detail="Email already in use")
    #     me.email = data.email

    # 2) смена пароля (с хэшированием)
    if data.password:
        me.hashed_password = password_helper.hash(data.password)

    # 3) сохранить
    await session.commit()
    await session.refresh(me)
    return me
            

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_me(
    user: User = Depends(current_active_user),
    manager: BaseUserManager[User, UUID] = Depends(get_user_manager),
):
    # Используем fastapi-users менеджер — корректные хуки, минимум кода.
    await manager.delete(user)
    return
######################################################
async def allow_psy_or_owner(me: User = Depends(current_active_user)) -> User:
    if me.role not in (UserRole.psychologist, UserRole.owner):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return me

@router.get("/{id}", response_model=UserRead, summary="Get user by id (psychologist/owner)")
async def get_user_by_id(
    id: UUID,
    _: User = Depends(allow_psy_or_owner),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(User).where(User.id == id)
    res = await session.execute(stmt)
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
#####################################################
async def allow_owner(me: User = Depends(current_active_user)) -> User:
    if me.role != UserRole.owner:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return me

class UserAdminUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None

@router.patch("/{id}", response_model=UserRead, summary="Update user by id (owner)")
async def update_user_by_id(
    id: UUID,
    data: UserAdminUpdate,
    _: User = Depends(allow_owner),
    session: AsyncSession = Depends(get_async_session),
):
    # 1) Найти пользователя
    res = await session.execute(select(User).where(User.id == id))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 2) Проверка уникальности email (если прилетел)
    if data.email is not None:
        email_exists = await session.execute(
            select(User.id).where(User.email == data.email, User.id != id)
        )
        if email_exists.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Email already in use")
        user.email = data.email

    # 3) Применить остальные поля
    if data.is_active is not None:
        user.is_active = data.is_active
    if data.role is not None:
        user.role = data.role

    await session.commit()
    await session.refresh(user)
    return user

@router.delete("/{id}", status_code=204, summary="Delete user by id (owner)")
async def delete_user_by_id(
    id: UUID,
    _: User = Depends(allow_owner),
    session: AsyncSession = Depends(get_async_session),
):
    res = await session.execute(select(User).where(User.id == id))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
    return None