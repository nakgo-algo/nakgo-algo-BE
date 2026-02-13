from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    title: str
    message: str
    is_read: bool
    createdAt: datetime

    @classmethod
    def from_orm_row(cls, row):
        return cls(
            id=row.id,
            type=row.type,
            title=row.title,
            message=row.message,
            is_read=row.is_read,
            createdAt=row.created_at,
        )


class UnreadCountResponse(BaseModel):
    count: int
