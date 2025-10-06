"""Authentication service handling password hashing, JWT tokens, and user authentication."""

import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException

from models import User
from config import settings


class AuthService:
    """Service class responsible for authentication operations."""
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt with a salt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a bcrypt hash."""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    
    def create_jwt_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT token with the given data and expiration time."""
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.access_token_expire_minutes
            )
        
        payload = data.copy()
        payload.update({"exp": expire})
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def decode_jwt_token(self, token: str) -> dict:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid authentication credentials: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def authenticate_user(self, email: str, password: str, user_repository) -> Optional[User]:
        """Authenticate a user with email and password."""
        user = user_repository.get_by_email(email)
        
        if not user or not self.verify_password(password, user.password):
            return None
        
        return user