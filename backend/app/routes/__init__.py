from fastapi import APIRouter

from app.auth.deps import fastapi_users, auth_backend, UserRead, UserCreate

from app.routes import profile as profile_router
from app.routes import account_delete
from app.routes import psychologist_profile
api = APIRouter(prefix="/api/v1")

# health
@api.get("/health")
async def health():
    return {"status": "ok"}

# profile (оставляем как есть; у него свой prefix внутри)
api.include_router(profile_router.router)

# --- auth из fastapi-users (логин/регистрация) ---
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

# --- наши кастомные /users (me и {id}) ---
api.include_router(account_delete.router)
api.include_router(psychologist_profile.router)