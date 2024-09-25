from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None
    password : str
    role: Optional[str] = "customer"

class UserOut(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None
    role: Optional[str] = None
    status: str

    class Config:
        orm_mode = True
