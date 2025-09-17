from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.db import get_db

app = FastAPI(title="TheraAI")
api = APIRouter(prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-ping")
def db_ping(db: Session = Depends(get_db)):
    value = db.execute(text("select 1")).scalar_one()
    return {"db": "ok", "value": value}

# Заглушки auth
@api.post("/auth/register")
def register():
    return {"access_token": "demo", "refresh_token": "demo", "token_type": "bearer"}

@api.post("/auth/login")
def login():
    return {"access_token": "demo", "refresh_token": "demo", "token_type": "bearer"}

# Заглушки users
@api.get("/users/me")
def me():
    return {"id": 1, "email": "user@example.com", "role": "user"}

# Заглушки billing
@api.get("/billing/plans")
def plans():
    return [
        {"code": "free", "name": "Free"},
        {"code": "start", "name": "Start"},
        {"code": "premium", "name": "Premium"},
    ]

@api.post("/billing/subscribe")
def subscribe():
    return {"ok": True}

@api.get("/billing/my")
def my():
    return {"plan": "free"}

app.include_router(api)
