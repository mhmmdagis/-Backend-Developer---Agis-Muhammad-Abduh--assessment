
from app.database import engine, Base, SessionLocal
from app.services import UserService
from app import models

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        svc = UserService(db)
        admin = db.query(models.User).filter(models.User.email=='admin@local').first()
        if not admin:
            svc.register('admin','admin@local','password123','admin')
            print('Created admin user (admin@local / password123)')
    finally:
        db.close()

if __name__ == '__main__':
    seed()
