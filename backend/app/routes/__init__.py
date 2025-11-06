from fastapi import APIRouter, Depends
from app.auth.deps import fastapi_users, auth_backend, current_active_user
from app.auth.deps import UserRead, UserCreate, UserUpdate
from app.models.user import User

# твои роутеры
from app.routes import profile as profile_router
from app.routes import account_delete

api = APIRouter()

# health
@api.get("/health")
async def health():
    return {"status": "ok"}

# profile (у тебя внутри profile_router уже свой prefix — оставляем как есть)
api.include_router(profile_router.router)

# fastapi-users
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

# наш кастомный DELETE /users/me
api.include_router(
    account_delete.router,
    prefix="/users",
)

api.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)



# дубль твоего GET /users/me, чтобы не потерялся
@api.get("/users/me", response_model=UserRead, tags=["users"])
async def read_me(user: User = Depends(current_active_user)):
    return user
