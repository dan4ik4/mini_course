from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi_users.manager import BaseUserManager
from app.core.db import get_db
from app.models.user import User
# импортни ту зависимость, где у тебя fastapi_users.current_user(active=True)
from app.auth.deps import current_active_user, get_user_manager # подгони путь при необходимости

router = APIRouter()

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_me(
    user: User = Depends(current_active_user),
    manager: BaseUserManager[User, UUID] = Depends(get_user_manager),
):
    # Используем fastapi-users менеджер — корректные хуки, минимум кода.
    await manager.delete(user)
    return