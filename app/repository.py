
from sqlalchemy.orm import Session
from app import models
from typing import Optional, List
from datetime import datetime

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, username: str, email: str, hashed_password: str, role: str="user"):
        user = models.User(username=username, email=email, hashed_password=hashed_password, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str):
        return self.db.query(models.User).filter(models.User.email==email).first()

    def get(self, user_id: int):
        return self.db.query(models.User).filter(models.User.id==user_id).first()

    def list(self, skip: int=0, limit: int=100):
        return self.db.query(models.User).offset(skip).limit(limit).all()

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, description: str=None, owner_id: int=None, attachment: str=None):
        task = models.Task(title=title, description=description, owner_id=owner_id, attachment=attachment)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get(self, task_id: int):
        return self.db.query(models.Task).filter(models.Task.id==task_id).first()

    def delete(self, task_id: int):
        task = self.get(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
        return task

    def update(self, task: models.Task, data: dict):
        for k,v in data.items():
            setattr(task,k,v)
        self.db.commit()
        self.db.refresh(task)
        return task

    def list(self, skip: int=0, limit: int=100, filters: dict=None) -> List[models.Task]:
        q = self.db.query(models.Task)
        if filters:
            if filters.get("status"):
                q = q.filter(models.Task.status==filters["status"])
            if filters.get("owner_id") is not None:
                q = q.filter(models.Task.owner_id==filters["owner_id"])
            if filters.get("q"):
                like = f"%{filters['q']}%"
                q = q.filter(models.Task.title.ilike(like) | models.Task.description.ilike(like))
        return q.offset(skip).limit(limit).all()

class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, token: str, expires_at):
        rt = models.RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
        self.db.add(rt)
        self.db.commit()
        self.db.refresh(rt)
        return rt

    def get(self, token: str):
        return self.db.query(models.RefreshToken).filter(models.RefreshToken.token==token).first()

    def delete(self, token: str):
        rt = self.get(token)
        if rt:
            self.db.delete(rt)
            self.db.commit()
        return rt
