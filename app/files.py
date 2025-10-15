
import os
from fastapi import UploadFile, HTTPException
from app.config import settings
from pathlib import Path
from typing import Tuple

def ensure_upload_dir():
    d = Path(settings.UPLOAD_DIR)
    d.mkdir(parents=True, exist_ok=True)
    return d

def validate_upload(file: UploadFile) -> Tuple[str,int]:
    allowed = [t.strip() for t in settings.ALLOWED_UPLOAD_TYPES.split(",")]
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="File type not allowed")
    data = file.file.read()
    size = len(data)
    if size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    file.file.seek(0)
    return file.content_type, size

def save_upload(file: UploadFile) -> str:
    ensure_upload_dir()
    validate_upload(file)
    filename = os.path.basename(file.filename)
    out_path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(out_path, "wb") as f:
        f.write(file.file.read())
    file.file.seek(0)
    return out_path
