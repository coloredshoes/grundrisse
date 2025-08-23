"""Source management routes."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from antidote import Provide

from sources import SourceService, Source, SourceCreate
from routes.dependencies import get_current_user


# Create router
router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("/", response_model=List[Source])
async def get_sources(
    username: str = Depends(get_current_user),
    source_service: SourceService = Provide[SourceService]
):
    """Get all sources."""
    return await source_service.get_all_sources()


@router.post("/", response_model=Source)
async def create_source(
    source: SourceCreate,
    username: str = Depends(get_current_user),
    source_service: SourceService = Provide[SourceService]
):
    """Create a new source."""
    return await source_service.create_source(source)


@router.delete("/{source_id}")
async def delete_source(
    source_id: str,
    username: str = Depends(get_current_user),
    source_service: SourceService = Provide[SourceService]
):
    """Delete a source."""
    success = await source_service.delete_source(source_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Source not found")
    
    return {"message": "Source deleted successfully"}
