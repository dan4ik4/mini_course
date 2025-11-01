# app/main.py
from fastapi import FastAPI, APIRouter, Depends, Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from app.auth.deps import fastapi_users, auth_backend, current_active_user
from app.auth.deps import UserRead, UserCreate, UserUpdate
from app.models.user import User
from app.routes import profile as profile_router

app = FastAPI(
    title="TheraAI",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    debug=True,
)

# единый префикс для API
api = APIRouter(prefix="/api/v1")

# health (под /api/v1/health)
@api.get("/health")
async def health():
    return {"status": "ok"}

# profile роуты под /api/v1/profile/...
api.include_router(profile_router.router)

# fastapi-users под /api/v1/auth/...
api.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# пример: текущий пользователь под /api/v1/users/me
@api.get("/users/me", response_model=UserRead, tags=["users"])
async def read_me(user: User = Depends(current_active_user)):
    return user

# подключаем весь api к приложению
app.include_router(api)

# ——— необязательная мидлварь для логов исключений ———
logger = logging.getLogger("uvicorn.error")
async def _log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception("UNHANDLED: %s", e)
        raise
app.add_middleware(BaseHTTPMiddleware, dispatch=_log_exceptions)
# ——————————————————————————————