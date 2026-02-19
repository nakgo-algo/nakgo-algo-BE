from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ModerationRequest(Base):
    __tablename__ = "moderation_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(String(200), nullable=False)
    matched_words: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")  # pending / resolved
    resolved_action: Mapped[str | None] = mapped_column(String(20), nullable=True)  # ignore / delete
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    post = relationship("Post")
