from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        password=user.password,  # Save hashed password
        role=user.role,
        status="active"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int = None, email: str = None):
    if user_id:
        return db.query(User).filter(User.id == user_id).first()
    if email:
        return db.query(User).filter(User.email == email).first()
    return None