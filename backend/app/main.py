from fastapi import FastAPI, APIRouter, Depends
from app.auth.deps import fastapi_users, auth_backend, current_active_user
from app.models.user import User
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

@app.get("/users/me", response_model=UserRead, tags=["users"])
async def read_me(user: User = Depends(current_active_user)):
    return user