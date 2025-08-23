"""Configuration management using Antidote DI and environment variables."""

import os
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv
from antidote import injectable, inject

# Load environment variables from .env file
# Try multiple locations to ensure .env is found
from pathlib import Path

def _load_env_file():
    """Load .env file from multiple possible locations."""
    current_dir = Path(__file__).parent
    possible_paths = [
        current_dir / ".env",  # Same directory as config.py
        current_dir.parent / ".env",  # Parent directory
        Path.cwd() / ".env",  # Current working directory
    ]
    
    for env_path in possible_paths:
        if env_path.exists():
            load_dotenv(env_path)
            print(f"Loaded environment from: {env_path}")
            return True
    
    print("Warning: No .env file found in expected locations")
    return False

# Load environment variables
_load_env_file()


def _require_env(var_name: str) -> str:
    """Require an environment variable to be set."""
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Required environment variable {var_name} is not set")
    return value


@injectable
@dataclass(frozen=True)
class DatabaseConfig:
    """EdgeDB database configuration."""
    host: str = os.getenv("EDGEDB_HOST", "localhost")
    port: int = int(os.getenv("EDGEDB_PORT", "5656"))
    database: str = os.getenv("EDGEDB_DATABASE", "grundrisse")
    user: Optional[str] = os.getenv("EDGEDB_USER")
    password: Optional[str] = os.getenv("EDGEDB_PASSWORD")


@injectable
@dataclass(frozen=True)
class AuthConfig:
    """Authentication configuration."""
    secret_key: str = os.getenv("SECRET_KEY") or _require_env("SECRET_KEY")
    algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_hours: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "24"))


@injectable
@dataclass(frozen=True)
class ServerConfig:
    """Server configuration."""
    host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    port: int = int(os.getenv("SERVER_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    cors_origins: list[str] = field(default_factory=lambda: os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","))


@injectable
@dataclass(frozen=True)
class AppConfig:
    """Main application configuration."""
    title: str = os.getenv("APP_TITLE", "Grundrisse Admin API")
    version: str = os.getenv("APP_VERSION", "1.0.0")
    description: str = os.getenv("APP_DESCRIPTION", "Admin interface for managing content sources")
    
    # Injected configurations
    database: DatabaseConfig = inject[DatabaseConfig]
    auth: AuthConfig = inject[AuthConfig]
    server: ServerConfig = inject[ServerConfig]
