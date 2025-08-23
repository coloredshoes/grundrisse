"""Authentication routes."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from antidote import inject

from auth import AuthService
from routes.dependencies import get_current_user


# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    username: str


# Create router
router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = inject[AuthService]
):
    """Authenticate user and return JWT token."""
    user = await auth_service.authenticate_user(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth_service.create_access_token(data={"sub": login_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(username: str = Depends(get_current_user)):
    """Get current user information."""
    return {"username": username}
