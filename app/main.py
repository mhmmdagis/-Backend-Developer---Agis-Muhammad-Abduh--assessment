
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, users, tasks
from app import models
import os

def create_app():
    app = FastAPI(title="Task Management API")
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(tasks.router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

app = create_app()


# Create DB tables automatically for development
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    pass
