
# Task Management API (FastAPI)

Features:
- FastAPI + SQLAlchemy
- JWT Authentication (access + refresh tokens)
- Role-based access (admin, manager, user)
- CRUD Task with filtering (by status, assignee, search)
- File upload with validation (max 2MB, allowed types)
- SQLite by default, PostgreSQL supported via DATABASE_URL
- Alembic included (run migrations manually)
- Tests with pytest

## Quick start (local)

```bash
unzip task_management_api_final.zip
cd task_management_api_final
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# (optional) edit .env
uvicorn app.main:app --reload
```

Open docs: http://127.0.0.1:8000/docs
