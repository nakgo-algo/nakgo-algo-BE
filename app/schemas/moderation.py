from datetime import datetime

from pydantic import BaseModel, Field


class ModerationListItem(BaseModel):
    id: int
    postTitle: str
    postContent: str
    postAuthor: str
    reason: str
    matchedWords: list[str]
    createdAt: datetime


class ModerationResolveRequest(BaseModel):
    action: str = Field(pattern=r"^(ignore|delete)$")
    deleteReason: str | None = None
