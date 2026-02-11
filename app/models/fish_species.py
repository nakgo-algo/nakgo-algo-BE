from sqlalchemy import Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class FishSpecies(Base):
    __tablename__ = "fish_species"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    min_length: Mapped[int] = mapped_column(Integer, nullable=False)
    banned_months: Mapped[list[int]] = mapped_column(JSON, nullable=False, default=list)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    fine: Mapped[str | None] = mapped_column(String(50), nullable=True)

    regulations = relationship("Regulation", back_populates="species")
