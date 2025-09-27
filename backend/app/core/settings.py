from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str = "SUPERSECRET"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()