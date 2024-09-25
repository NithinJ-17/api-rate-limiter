from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserOut
from app.auth import get_current_user  # Import the get_current_user function
from app.crud import create_user, get_user

router = APIRouter()

@router.post("/users/", response_model=UserOut, tags=["User Operations"])
def create_new_user(user: UserCreate, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    db_user = create_user(db=db, user=user)
    return db_user

@router.get("/users/{user_id}", response_model=UserOut, tags=["User Operations"])
def retrieve_user(user_id: int, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    db_user = get_user(db, user_id=user_id)  # Now correctly retrieves by user_id
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

