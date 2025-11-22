from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    login_id: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    login_id: str
    password: str

# --- NEW SCHEMA ---
class UserPasswordUpdate(BaseModel):
    login_id: str
    current_password: str
    new_password: str

class UserResponse(BaseModel):
    id: int
    login_id: str
    email: str

    class Config:
        from_attributes = True