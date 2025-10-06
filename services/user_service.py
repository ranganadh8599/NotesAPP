"""User service handling business logic for user operations."""

from datetime import datetime, timezone
from fastapi import HTTPException

from models import User, UserCreate, UserResponse, generate_id
from repositories.user_repository import UserRepository
from services.auth_service import AuthService


class UserService:
    """Service class handling user-related business logic."""
    
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user account."""
        # Check if user already exists
        if self.user_repository.exists_by_email(user_data.user_email):
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        
        # Create new user
        now = datetime.now(timezone.utc)
        user = User(
            user_id=generate_id(),
            user_name=user_data.user_name,
            user_email=user_data.user_email,
            password=self.auth_service.hash_password(user_data.password),
            created_on=now,
            last_update=now
        )
        
        self.user_repository.create(user)
        
        return UserResponse(
            user_id=user.user_id,
            user_name=user.user_name,
            user_email=user.user_email,
            created_on=user.created_on,
            last_update=user.last_update
        )
    
    def get_user_info(self, user: User) -> UserResponse:
        """Get user information for response."""
        return UserResponse(
            user_id=user.user_id,
            user_name=user.user_name,
            user_email=user.user_email,
            created_on=user.created_on,
            last_update=user.last_update
        )