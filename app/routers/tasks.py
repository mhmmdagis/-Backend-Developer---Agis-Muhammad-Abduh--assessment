
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.database import get_db
from sqlalchemy.orm import Session
from app.services import TaskService
from app.deps import get_current_user, require_role
from app.files import save_upload

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current = Depends(get_current_user)):
    svc = TaskService(db)
    task = svc.create_task(payload.title, payload.description, owner_id=payload.owner_id or current.id)
    return task

@router.get("/", response_model=list[TaskResponse])
def list_tasks(skip: int=0, limit: int=100, status: str|None=None, owner_id: int|None=None, q: str|None=None, db: Session = Depends(get_db)):
    svc = TaskService(db)
    filters = {}
    if status: filters['status'] = status
    if owner_id is not None: filters['owner_id'] = owner_id
    if q: filters['q'] = q
    return svc.list_tasks(skip=skip, limit=limit, filters=filters)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    svc = TaskService(db)
    task = svc.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), current = Depends(get_current_user)):
    svc = TaskService(db)
    task = svc.update_task(task_id, payload.dict(exclude_unset=True))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db), current = Depends(require_role("manager"))):
    svc = TaskService(db)
    deleted = svc.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": True}

@router.post("/{task_id}/upload", response_model=TaskResponse)
def upload_attachment(task_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current = Depends(get_current_user)):
    svc = TaskService(db)
    task = svc.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    path = save_upload(file)
    task = svc.update_task(task_id, {"attachment": path})
    return task
