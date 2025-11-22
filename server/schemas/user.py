from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    login_id: str
    email: EmailStr
    password: str

# --- NEW SCHEMA ---
class UserLogin(BaseModel):
    login_id: str
    password: str

class UserResponse(BaseModel):
    id: int
    login_id: str
    email: str

    class Config:
        from_attributes = True # Updated for Pydantic v2 compatibility