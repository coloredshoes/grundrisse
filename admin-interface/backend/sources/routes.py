"""Sources routes."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from antidote import inject

from auth.routes import get_current_user
from auth.models import User
from sources.models import Source, SourceCreate
from sources.service import SourceService

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("/", response_model=List[Source])
async def get_sources(
    current_user: User = Depends(get_current_user),
    source_service: SourceService = inject[SourceService]
):
    """Get all sources."""
    return await source_service.get_all_sources()


@router.post("/", response_model=Source)
async def create_source(
    source_data: SourceCreate,
    current_user: User = Depends(get_current_user),
    source_service: SourceService = inject[SourceService]
):
    """Create a new source."""
    return await source_service.create_source(source_data)


@router.delete("/{source_id}")
async def delete_source(
    source_id: str,
    current_user: User = Depends(get_current_user),
    source_service: SourceService = inject[SourceService]
):
    """Delete a source."""
    success = await source_service.delete_source(source_id)
    if not success:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"message": "Source deleted successfully"}
