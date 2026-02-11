from datetime import datetime

from pydantic import BaseModel, Field


class PointCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    lat: float
    lng: float
    memo: str | None = None
    color: str | None = None


class PointResponse(BaseModel):
    id: int
    name: str
    lat: float
    lng: float
    memo: str | None = None
    color: str | None = None
    createdAt: datetime
