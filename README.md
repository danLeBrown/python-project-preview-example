# Preview Example API

A minimal FastAPI example for preview environments: Postgres, Redis, health check, and an admin seeder.

## Setup

1. **Environment**

   Copy `.env.example` to `.env` and set:

   - `DATABASE_URL` – Postgres connection (async): `postgresql+asyncpg://user:password@host:5432/dbname`
   - `REDIS_URL` – Redis connection: `redis://host:6379/0`

2. **Install**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Run**

   Ensure Postgres and Redis are running, then:

   ```bash
   # Seed admin users (optional; creates tables if missing)
   python -m scripts.seed_admin

   # Start the API
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Endpoints

- `GET /` – Welcome and link to docs
- `GET /health` – Health check (DB + Redis status)
- `GET /docs` – Swagger UI
- `GET /items`, `POST /items`, `GET /items/{id}` – Example CRUD (items in Postgres)
- `GET /items/stats/requests` – Request counter (Redis)
- `GET /admins` – List seeded admins

## For Preview Tooling

This repo is intended as a reference for a tool that spins up previews of Python projects. It demonstrates:

- **Postgres** – `DATABASE_URL`, SQLAlchemy async, tables created on app startup
- **Redis** – `REDIS_URL`, used for a simple counter
- **`.env`** – `REDIS_URL` and `DATABASE_URL` are the only required vars
- **Health** – `/health` reports database and Redis status
- **Seeder** – `python -m scripts.seed_admin` runs independently and seeds admin users
