from fastapi import APIRouter

from app.auth.deps import fastapi_users, auth_backend

from app.routes import profile as profile_router
from app.routes import users_me
from app.routes import users_admin
from app.routes import psychologist_profile
from app.schemas.user import UserRead, UserCreate

api = APIRouter(prefix="/api/v1")

# health
@api.get("/health")
async def health():
    return {"status": "ok"}

# profile
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
api.include_router(users_me.router)
api.include_router(users_admin.router)
api.include_router(psychologist_profile.router)