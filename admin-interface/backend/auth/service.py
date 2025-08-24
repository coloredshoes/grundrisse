"""Auth service with authentication and JWT management."""

import hashlib
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from antidote import injectable, inject

from config import AuthConfig
from database import DatabaseService
from auth.models import User

# Import generated queries
from auth.queries import authenticate_user


security = HTTPBearer()


@injectable
class AuthService:
    """Authentication service with JWT token management."""
    
    def __init__(
        self, 
        config: AuthConfig = inject[AuthConfig],
        db: DatabaseService = inject[DatabaseService]
    ):
        self.config = config
        self.db = db
    
    def create_access_token(self, data: dict) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=self.config.access_token_expire_hours)
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode, 
            self.config.secret_key, 
            algorithm=self.config.algorithm
        )
        return encoded_jwt
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials) -> str:
        """Verify JWT token and return username."""
        try:
            payload = jwt.decode(
                credentials.credentials, 
                self.config.secret_key, 
                algorithms=[self.config.algorithm]
            )
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return username
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    async def authenticate_user_login(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        client = await self.db.get_client()
        users = await authenticate_user(
            client,
            username=username,
            password_hash=password_hash
        )
        
        if users:
            # authenticate_user returns a list, get the first user
            user = users[0]
            return User(username=user.username)
        return None
