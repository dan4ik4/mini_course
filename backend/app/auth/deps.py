import uuid
from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi_users import FastAPIUsers, schemas
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.manager import BaseUserManager, UUIDIDMixin
from fastapi_users.jwt import SecretType
from starlette.requests import Request

from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel, EmailStr, ConfigDict

from app.core.settings import settings
from app.db.session import AsyncSessionLocal
from app.models.user import User, UserRole

from typing import Optional
# ---------- session dep ----------
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# ---------- user db ----------
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


# ---------- pydantic схемы ----------
class UserRead(schemas.BaseUser[uuid.UUID]):
    role: UserRole


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    role: UserRole = UserRole.user


class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_superuser: Optional[bool] = None


# ---------- user manager ----------
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret: SecretType = settings.JWT_SECRET
    verification_token_secret: SecretType = settings.JWT_SECRET

    async def on_after_register(self, user: User, request: Request | None = None):
        return


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


# ---------- JWT backend ----------
#class SimpleJWTStrategy(Strategy[User, uuid.UUID]):
#    def __init__(self, secret: str, lifetime_seconds: int = 3600):
#        self.secret = secret
#        self.lifetime_seconds = lifetime_seconds
#
#    async def write_token(self, user: User) -> str:
#        data = {"sub": str(user.id)}
#        return generate_jwt(data, self.secret, lifetime_seconds=self.lifetime_seconds)
#
#    async def read_token(self, token: str, request: Request | None = None) -> uuid.UUID | None:
#        try:
#            data = decode_jwt(token, self.secret)
#            return uuid.UUID(data.get("sub"))
#        except Exception:
#            return None


#def get_jwt_strategy() -> Strategy[User, uuid.UUID]:
    # сутки
#    return SimpleJWTStrategy(settings.JWT_SECRET, lifetime_seconds=60 * 60 * 24)


#bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

#auth_backend = AuthenticationBackend(
#    name="jwt",
#    transport=bearer_transport,
#    get_strategy=get_jwt_strategy,
#)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=60 * 60 * 24)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


# ---------- FastAPI Users instance + deps ----------
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)


# простая проверка роли (owner как суперюзер пройдёт автоматически)
def require_role(*allowed: UserRole):
    async def dep(user: User = Depends(current_active_user)):
        if user.is_superuser:
            return user
        if user.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user
    return dep
