from fastapi import FastAPI, APIRouter
from app.auth.deps import (
    fastapi_users, auth_backend,
    UserRead, UserCreate, UserUpdate,
)

app = FastAPI(title="TheraAI")

# заготовка под твои ручки (папки api нет — и не нужна)
api = APIRouter(prefix="/api/v1")

@api.get("/health")
async def health():
    return {"status": "ok"}

# подключаем заготовку
app.include_router(api)

# подключаем fastapi-users
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
