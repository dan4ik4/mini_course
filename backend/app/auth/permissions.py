from fastapi import Depends, HTTPException, status

from app.auth.deps import current_active_user
from app.models.user import User, UserRole


def require_owner(user: User = Depends(current_active_user)) -> User:
    if user.role != UserRole.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions (owner only)",
        )
    return user


def require_teacher(user: User = Depends(current_active_user)) -> User:
    if user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions (teacher only)",
        )
    return user


def require_owner_or_teacher(user: User = Depends(current_active_user)) -> User:
    if user.role not in (UserRole.teacher, UserRole.owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions (owner or teacher required)",
        )
    return user
