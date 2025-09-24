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


## Команды
docker-compose up -d db
python backend/db_ping.py
alembic revision -m "create users" --autogenerate
alembic upgrade head
