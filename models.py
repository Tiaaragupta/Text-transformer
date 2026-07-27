"""
ORM models (SQLModel = Pydantic validation + SQLAlchemy table, in one class).

Sprint 3 goal: "Schema Design" -> proper data types, constraints, and a
schema that reflects the `transformations` table called out in the
blueprint (id, original_text, transformed_text, created_at).
"""

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Transformation(SQLModel, table=True):
    """One row = one text-processing request and its result."""

    id: Optional[int] = Field(default=None, primary_key=True)
    original_text: str = Field(nullable=False)
    transformed_text: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class TransformRequest(SQLModel):
    """Request body schema for POST /transform (not a table - just validation)."""

    text: str
    mode: str = "uppercase"  # uppercase | reverse | title


class TransformResponse(SQLModel):
    """Response schema for POST /transform."""

    id: int
    original_text: str
    transformed_text: str
    created_at: datetime
