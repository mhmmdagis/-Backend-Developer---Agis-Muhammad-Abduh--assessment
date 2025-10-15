
from datetime import datetime, timedelta, timezone
from app.repository import UserRepository, TaskRepository, RefreshTokenRepository
from app.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app import models
from app.config import settings
from sqlalchemy.orm import Session

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.rt_repo = RefreshTokenRepository(db)

    def register(self, username: str, email: str, password: str, role: str="user"):
        if self.user_repo.get_by_email(email):
            raise ValueError("Email already registered")
        hashed = get_password_hash(password)
        user = self.user_repo.create(username=username, email=email, hashed_password=hashed, role=role)
        return user

    def authenticate(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        access = create_access_token({"user_id": user.id, "email": user.email, "role": user.role}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh = create_refresh_token()
        expires = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        self.rt_repo.create(user_id=user.id, token=refresh, expires_at=expires)
        return {"access_token": access, "refresh_token": refresh, "user": user}

    def refresh(self, token: str):
        rt = self.rt_repo.get(token)
        if not rt:
            return None
        expires_at = rt.expires_at
        if expires_at is not None and expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at is None or expires_at < datetime.now(timezone.utc):
            return None
        user = self.user_repo.get(rt.user_id)
        access = create_access_token({"user_id": user.id, "email": user.email, "role": user.role}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access}

class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repo = TaskRepository(db)

    def create_task(self, title: str, description: str=None, owner_id: int=None, attachment: str=None):
        return self.task_repo.create(title=title, description=description, owner_id=owner_id, attachment=attachment)

    def get_task(self, task_id: int):
        return self.task_repo.get(task_id)

    def update_task(self, task_id: int, data: dict):
        task = self.get_task(task_id)
        if not task:
            return None
        return self.task_repo.update(task, data)

    def delete_task(self, task_id: int):
        return self.task_repo.delete(task_id)

    def list_tasks(self, skip: int=0, limit: int=100, filters: dict=None):
        return self.task_repo.list(skip=skip, limit=limit, filters=filters)
