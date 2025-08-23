"""Source management service."""

from typing import List
from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel
from antidote import injectable, inject
import edgedb

from database import DatabaseService


class Source(BaseModel):
    id: str
    name: str
    type: str
    url: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class SourceCreate(BaseModel):
    name: str
    type: str
    url: str


@injectable
class SourceService:
    """Service for managing content sources."""
    
    def __init__(self, db: DatabaseService = inject[DatabaseService]):
        self.db = db
    
    async def get_all_sources(self) -> List[Source]:
        """Get all sources ordered by creation date."""
        client = await self.db.get_client()
        sources = await client.query("""
            SELECT Source {
                id,
                name,
                type,
                url,
                is_active,
                created_at,
                updated_at
            }
            ORDER BY .created_at DESC
        """)
        
        return [
            Source(
                id=str(source.id),
                name=source.name,
                type=source.type,
                url=source.url,
                is_active=source.is_active,
                created_at=source.created_at,
                updated_at=source.updated_at
            )
            for source in sources
        ]
    
    async def create_source(self, source_data: SourceCreate) -> Source:
        """Create a new source."""
        client = await self.db.get_client()
        
        # Insert new source
        new_source = await client.query_single("""
            INSERT Source {
                name := <str>$name,
                type := <str>$type,
                url := <str>$url
            }
        """, name=source_data.name, type=source_data.type, url=source_data.url)
        
        # Fetch the complete source with all fields
        complete_source = await client.query_single("""
            SELECT Source {
                id,
                name,
                type,
                url,
                is_active,
                created_at,
                updated_at
            }
            FILTER .id = <uuid>$id
        """, id=new_source.id)
        
        return Source(
            id=str(complete_source.id),
            name=complete_source.name,
            type=complete_source.type,
            url=complete_source.url,
            is_active=complete_source.is_active,
            created_at=complete_source.created_at,
            updated_at=complete_source.updated_at
        )
    
    async def delete_source(self, source_id: str) -> bool:
        """Delete a source by ID."""
        client = await self.db.get_client()
        
        try:
            deleted = await client.query_single("""
                DELETE Source
                FILTER .id = <uuid>$source_id
            """, source_id=source_id)
            
            return deleted is not None
        except edgedb.InvalidValueError:
            raise HTTPException(status_code=400, detail="Invalid source ID format")
