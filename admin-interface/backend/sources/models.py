"""Sources module models."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SourceCreate(BaseModel):
    """Request model for creating a source."""
    name: str
    type: str
    url: str


class Source(BaseModel):
    """Source model."""
    id: str
    name: str
    type: str
    url: str
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
