
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserCreate, Token, RefreshRequest
from app.services import UserService
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Form

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=dict)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    svc = UserService(db)
    try:
        user = svc.register(payload.username, payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": user.id, "email": user.email}

@router.post("/login", response_model=Token)
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    svc = UserService(db)
    auth = svc.authenticate(email, password)
    if not auth:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": auth["access_token"], "refresh_token": auth["refresh_token"], "token_type": "bearer"}

@router.post("/refresh", response_model=dict)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    svc = UserService(db)
    new = svc.refresh(body.refresh_token)
    if not new:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    return new
