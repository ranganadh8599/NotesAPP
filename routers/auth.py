"""Authentication routes for user signup, signin, and user info."""

from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends

from models import UserCreate, UserLogin, Token, User
from services.auth_service import AuthService
from services.user_service import UserService
from repositories.user_repository import UserRepository
from dependencies import get_auth_service, get_user_service, get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", summary="Create a new user account")
async def signup(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """
    Create a new user account with email and password.
    
    - **user_name**: The user's display name
    - **user_email**: The user's email address (must be unique)
    - **password**: The user's password (will be hashed before storage)
    """
    return user_service.create_user(user_data)


@router.post("/signin", response_model=Token, summary="Sign in with email and password")
async def signin(
    credentials: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
    user_repo: UserRepository = Depends(lambda: UserRepository())
):
    """
    Authenticate user and return access token.
    
    - **user_email**: The user's email address
    - **password**: The user's password
    
    Returns a JWT access token that should be included in subsequent requests.
    """
    user = auth_service.authenticate_user(credentials.user_email, credentials.password, user_repo)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_jwt_token(
        data={"sub": user.user_email},
        expires_delta=timedelta(minutes=auth_service.access_token_expire_minutes)
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", summary="Get current user information")
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Get information about the currently authenticated user.
    
    Requires a valid JWT token in the Authorization header.
    """
    return user_service.get_user_info(current_user)