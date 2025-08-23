"""Authentication service with JWT token management."""

import hashlib
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from antidote import injectable, inject

from config import AuthConfig
from database import DatabaseService


security = HTTPBearer()


@injectable
class AuthService:
    """Authentication service for JWT token management."""
    
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
        expire = datetime.now(datetime.UTC) + timedelta(hours=self.config.access_token_expire_hours)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)
        return encoded_jwt
    
    async def verify_token(self, credentials: HTTPAuthorizationCredentials) -> str:
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
    
    async def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """Authenticate user with username and password."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        client = await self.db.get_client()
        user = await client.query_single("""
            SELECT User {
                username
            }
            FILTER .username = <str>$username AND .password_hash = <str>$password_hash
        """, username=username, password_hash=password_hash)
        
        if user:
            return {"username": user.username}
        return None
