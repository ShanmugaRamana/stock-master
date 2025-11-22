from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from core.database import Base

class User(Base):
    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True, index=True)
    login_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # --- NEW COLUMNS ---
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())