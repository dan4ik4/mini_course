import os, time
import jwt  # PyJWT
from passlib.hash import pbkdf2_sha256

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALGO = "HS256"
JWT_TTL_SEC = 24 * 60 * 60  # 24h

def hash_password(p: str) -> str:
    return pbkdf2_sha256.hash(p)

def verify_password(p: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(p, hashed)

def create_token(user_id: int, role: str) -> str:
    now = int(time.time())
    payload = {"sub": str(user_id), "role": role, "iat": now, "exp": now + JWT_TTL_SEC}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])