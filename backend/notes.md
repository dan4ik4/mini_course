# DEV NOTES

## Роли
- user
- psychologist
- owner (полный доступ)

## Прогресс шагов
- [x] Подняли Postgres (docker-compose, проверка `db_ping.py`)
- [x] Настроили .env (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)
- [x] Сделали модель User (id, email, password_hash, role, is_active, created_at)
- [ ] Alembic: прогнали миграцию create users
- [ ] Реализовать регистрацию (по умолчанию user, первый юзер = owner)
- [ ] Логин через JWT
- [ ] Проверка ролей (current_user, psych_only, owner_only)
- [ ] CRUD для пользователей (me, список всех, смена роли)
- [ ] Подготовить основу админки

## Команды, которые запускали
```bash
docker-compose up -d db
python backend/db_ping.py
alembic revision -m "create users" --autogenerate
alembic upgrade head

## Прогресс
[x] Подняли Postgres и db_ping.py = OK
[x] Настроили alembic/env.py (target_metadata=Base.metadata, url из .env)
[x] Создали миграцию users и сделали upgrade head
[x] deps: passlib==1.7.4, PyJWT==2.9.0, python-dotenv
(перешли на pure-Python, чтобы не собирать bcrypt/cryptography на Win+Py3.13)
[x] core/security.py: PBKDF2 hash + JWT (HS256), .env -> JWT_SECRET
[x] app/core/db.py — добавили Base(DeclarativeBase)
[x] env.py — target_metadata = Base.metadata, импорт app.models.user
[x] Пересоздали миграцию users → теперь в upgrade() есть op.create_table
[x] alembic upgrade head → таблица users в БД
[x] create_owner_sql.py → успешно создан первый пользователь с ролью owner
[x] Создан app/core/settings.py (pydantic-settings)  
[x] Создан app/db/session.py (async engine + async_sessionmaker)  
[x] Переписан app/models/user.py под fastapi-users (UUID PK, hashed_password, роли user/psychologist/owner, created_at)  
реализована рабочая JWT-аутентификация через FastAPI Users;
подключены эндпоинты /auth/register, /auth/jwt/login, /auth/jwt/logout, /users/me;
исправлены миграции и структура таблицы users (UUID, hashed_password, роли, флаги активности);
добавлены схемы UserRead, UserCreate, UserUpdate на основе BaseUser из fastapi-users;
защищённые роуты теперь требуют Bearer-токен (без авторизации возвращают 401);
проверено: регистрация → логин → авторизация → /users/me возвращает корректного юзера;
Исправлено подключение к PostgreSQL (ошибка 10061, Docker теперь стабильно активен).
.env обновлён: DB_HOST=127.0.0.1, добавлен корректный DATABASE_URL.
Добавлена одно-к-одному связь между User и Profile (user.profile, profile.user).
Приведены типы (user_id → UUID), исправлены импорты в profile.py.
Проверено: регистрация и логин работают, /api/v1/profile/me возвращает корректные данные.
Swagger UI работает стабильно.
Следующий шаг: реализовать PATCH /api/v1/profile/me (редактирование профиля) и DELETE /api/v1/users/me (удаление пользователя).

## Команды
docker-compose up -d db
python backend/db_ping.py
alembic revision -m "create users" --autogenerate
alembic upgrade head

357a3c2a-2d89-4440-8022-f141ff265268
0d1f49fd-e6dc-4bf5-bf78-79874e47d8f9
d9146898-fa46-4f63-90e3-b850754d3c9b



"""add sessions table

Revision ID: db3285631796
Revises: XXXX_initial
Create Date: 2025-12-04 17:40:28.681466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_users_db_sqlalchemy.generics import GUID

# revision identifiers, used by Alembic.
revision: str = 'db3285631796'
down_revision: Union[str, Sequence[str], None] = 'b753a375f3e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TYPE sessionstatus AS ENUM (
        'requested',
        'approved',
        'rejected',
        'canceled',
        'finished'
    )
""")

op.create_table(
    'sessions',
    sa.Column('id', GUID(), primary_key=True),
    sa.Column('user_id', GUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    sa.Column('psychologist_id', GUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    sa.Column('scheduled_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('status', sa.Enum(name="sessionstatus"), nullable=False, server_default='requested'),
    sa.Column('jitsi_url', sa.String(length=512), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
)


def downgrade() -> None:
    op.drop_table('sessions')
op.execute("DROP TYPE sessionstatus")