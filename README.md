# mini_course
Mini-USOS Backend

Backend projektu zaliczeniowego systemu rejestracji na zajęcia (uproszczony system typu USOS).
Projekt został zrealizowany przy użyciu FastAPI, PostgreSQL, SQLAlchemy (async), Alembic oraz JWT.

Do uruchomienia projektu wymagane są:
- Python 3.11+
- Docker oraz Docker Compose

1. Klonowanie repozytorium

git clone <repo_url>
cd <repo_name>

2. Konfiguracja zmiennych środowiskowych

W katalogu głównym projektu należy utworzyć plik .env o następującej zawartości:

DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=app
DB_USER=app
DB_PASS=app
JWT_SECRET=dev-secret-change-me
DATABASE_URL=postgresql+psycopg2://app:app@127.0.0.1:5432/app

3. Uruchomienie bazy danych PostgreSQL

docker-compose up -d

4. Instalacja zależności Pythona

pip install -r requirements.txt

lub alternatywnie:

pip install fastapi uvicorn sqlalchemy asyncpg alembic fastapi-users[sqlalchemy,jwt]

5. Wykonanie migracji bazy danych

alembic upgrade head

6. Uruchomienie serwera aplikacji

uvicorn app.main:app --reload

Aplikacja będzie dostępna pod adresem:
http://127.0.0.1:8000

Dokumentacja API (Swagger):
http://127.0.0.1:8000/docs

Struktura aplikacji opiera się na podziale na warstwy:
- models (modele bazy danych)
- schemas (schematy Pydantic)
- routes (endpointy API)
- core (konfiguracja, baza danych, bezpieczeństwo)

Na obecnym etapie projektu zaimplementowano:
- architekturę backendu
- połączenie z bazą PostgreSQL
- migracje Alembic
- model użytkownika
- autoryzację JWT
- role użytkowników (student, teacher, admin)

Projekt jest w trakcie dalszego rozwoju.
