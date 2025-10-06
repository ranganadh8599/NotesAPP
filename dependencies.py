"""App dependency setup."""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models import User
from services.auth_service import AuthService
from services.user_service import UserService
from services.note_service import NoteService
from repositories.user_repository import UserRepository
from repositories.note_repository import NoteRepository


# Security
security = HTTPBearer()

# Repository instances
user_repository = UserRepository()
note_repository = NoteRepository()

# Service instances
auth_service = AuthService()
user_service = UserService(user_repository, auth_service)
note_service = NoteService(note_repository)


def get_auth_service() -> AuthService:
    """Dependency to get the auth service."""
    return auth_service


def get_user_service() -> UserService:
    """Dependency to get the user service."""
    return user_service


def get_note_service() -> NoteService:
    """Dependency to get the note service."""
    return note_service


def get_user_repository() -> UserRepository:
    """Dependency to get the user repository."""
    return user_repository


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
    user_repo: UserRepository = Depends(get_user_repository)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.
    
    This function extracts the JWT token from the request header,
    validates it, and returns the authenticated user.
    """
    token = credentials.credentials
    payload = auth_service.decode_jwt_token(token)
    
    user_email = payload.get("sub")
    if user_email is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = user_repo.get_by_email(user_email)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user