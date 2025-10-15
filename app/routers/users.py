
from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, UserResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app.services import UserService
from app.deps import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db), current = Depends(require_role("admin"))):
    svc = UserService(db)
    user = svc.register(payload.username, payload.email, payload.password)
    return user

@router.get("/me", response_model=UserResponse)
def me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[UserResponse])
def list_users(skip: int=0, limit: int=100, db: Session = Depends(get_db), current = Depends(require_role("admin"))):
    svc = UserService(db)
    return svc.user_repo.list(skip, limit)
