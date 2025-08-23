"""Database service with EdgeDB client management."""

import hashlib
from typing import Optional
import edgedb
from antidote import injectable, inject
from config import DatabaseConfig


@injectable
class DatabaseService:
    """EdgeDB database service with connection management."""
    
    def __init__(self, config: DatabaseConfig = inject[DatabaseConfig]):
        self.config = config
        self._client: Optional[edgedb.AsyncIOClient] = None
    
    async def get_client(self) -> edgedb.AsyncIOClient:
        """Get or create EdgeDB client."""
        if self._client is None:
            self._client = edgedb.create_async_client(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
            )
        return self._client
    
    async def close(self):
        """Close database connection."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def initialize(self):
        """Initialize database with default data."""
        client = await self.get_client()
        
        # Create default admin user if it doesn't exist
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        
        await client.query("""
            INSERT User {
                username := 'admin',
                password_hash := <str>$password_hash
            } UNLESS CONFLICT ON .username
        """, password_hash=password_hash)
