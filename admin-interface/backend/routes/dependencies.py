"""Common dependencies for route handlers."""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from antidote import inject

from auth import AuthService, security


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = inject[AuthService]
) -> str:
    """Dependency to get current authenticated user."""
    return await auth_service.verify_token(credentials)
