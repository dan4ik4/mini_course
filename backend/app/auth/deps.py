import uuid
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.manager import BaseUserManager, UUIDIDMixin
from fastapi_users.jwt import SecretType
from starlette.requests import Request

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.models.user import User
from app.db.session import get_db

# ---------- user db ----------
async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)


# ---------- user manager ----------
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret: SecretType = settings.JWT_SECRET
    verification_token_secret: SecretType = settings.JWT_SECRET

    async def on_after_register(self, user: User, request: Request | None = None):
        return


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="/api/v1/auth/jwt/login")

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