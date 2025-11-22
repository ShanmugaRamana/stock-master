from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import secrets
from core.database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse, UserLogin, UserPasswordUpdate
from core.email_utils import send_verification_email

router = APIRouter(tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
@router.post("/signup", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.login_id == user.login_id).first():
        raise HTTPException(status_code=400, detail="Login ID already taken")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    token = secrets.token_urlsafe(32)

    new_user = User(
        login_id=user.login_id,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_verified=False,
        verification_token=token
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_verification_email(user.email, token)

    return new_user

# --- NEW VERIFICATION ROUTE ---
@router.get("/verify", response_class=HTMLResponse)
def verify_account(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    
    if not user:
        return """
        <html>
            <body style='font-family: Arial; text-align: center; padding-top: 50px;'>
                <h1 style='color: red;'>Invalid or Expired Link</h1>
                <p>Please contact support.</p>
            </body>
        </html>
        """

    if user.is_verified:
        return """
        <html>
            <body style='font-family: Arial; text-align: center; padding-top: 50px;'>
                <h1 style='color: #10B981;'>Already Verified!</h1>
                <p>You can return to the Stock Master application and login.</p>
            </body>
        </html>
        """

    # Verify the user
    user.is_verified = True
    user.verification_token = None  # Clear token so it can't be used again
    db.commit()

    return """
    <html>
        <body style='font-family: Arial; text-align: center; padding-top: 50px;'>
            <h1 style='color: #10B981;'>Verification Successful!</h1>
            <p>Your account is now active.</p>
            <p>Please return to the Stock Master app to login.</p>
        </body>
    </html>
    """
@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # 1. Find User
    user = db.query(User).filter(User.login_id == user_data.login_id).first()
    
    # 2. Check if User exists and Password matches
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Login ID or Password")
    
    # 3. Check Verification Status
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Account not verified. Please check your email.")

    return {"message": "Login Successful", "user_id": user.id, "username": user.login_id, "email": user.email}

@router.post("/update-password")
def update_password(data: UserPasswordUpdate, db: Session = Depends(get_db)):
    # 1. Find User
    user = db.query(User).filter(User.login_id == data.login_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 2. Verify Current Password
    if not verify_password(data.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    
    # 3. Hash and Save New Password
    user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}