"""Sources service for managing content sources."""

from datetime import datetime
from typing import List
from fastapi import HTTPException
from antidote import injectable, inject
import edgedb

from database import DatabaseService
from sources.models import Source, SourceCreate

# Import generated queries
from sources.queries import (
    get_all_sources,
    create_source as create_source_query,
    get_source_by_id,
    delete_source as delete_source_query
)


@injectable
class SourceService:
    """Service for managing content sources."""
    
    def __init__(self, db: DatabaseService = inject[DatabaseService]):
        self.db = db
    
    async def get_all_sources(self) -> List[Source]:
        """Get all sources ordered by creation date."""
        client = await self.db.get_client()
        sources = await get_all_sources(client)
        
        return [
            Source(
                id=str(source.id),
                name=source.name,
                type=source.type,
                url=source.url,
                is_active=source.is_active or False,
                created_at=source.created_at or datetime.now(),
                updated_at=source.updated_at or datetime.now()
            )
            for source in sources
        ]
    
    async def create_source(self, source_data: SourceCreate) -> Source:
        """Create a new source."""
        client = await self.db.get_client()
        
        # Insert new source using generated query
        new_source = await create_source_query(
            client,
            name=source_data.name,
            type=source_data.type,
            url=source_data.url
        )
        
        # Fetch the complete source with all fields
        complete_source = await get_source_by_id(
            client,
            source_id=new_source.id
        )
        
        if not complete_source:
            raise HTTPException(status_code=500, detail="Failed to create source")
        
        source = complete_source[0]  # get_source_by_id returns a list
        return Source(
            id=str(source.id),
            name=source.name,
            type=source.type,
            url=source.url,
            is_active=source.is_active or False,
            created_at=source.created_at or datetime.now(),
            updated_at=source.updated_at or datetime.now()
        )
    
    async def delete_source(self, source_id: str) -> bool:
        """Delete a source by ID."""
        client = await self.db.get_client()
        
        try:
            deleted = await delete_source_query(
                client,
                source_id=source_id
            )
            
            return deleted is not None
        except edgedb.InvalidValueError:
            raise HTTPException(status_code=400, detail="Invalid source ID format")
