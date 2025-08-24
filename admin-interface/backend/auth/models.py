"""Auth module models."""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Request model for user login."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Response model for authentication token."""
    access_token: str
    token_type: str = "bearer"


class User(BaseModel):
    """User model."""
    username: str
