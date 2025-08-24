"""Auth routes."""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from antidote import inject

from auth.models import LoginRequest, TokenResponse, User
from auth.service import AuthService, security

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = inject[AuthService]
):
    """Authenticate user and return JWT token."""
    user = await auth_service.authenticate_user_login(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth_service.create_access_token(data={"sub": login_data.username})
    return TokenResponse(access_token=access_token)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = inject[AuthService]
) -> User:
    """Get current authenticated user from JWT token."""
    username = auth_service.verify_token(credentials)
    return User(username=username)
