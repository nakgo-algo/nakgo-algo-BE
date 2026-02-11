from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Regulation(Base):
    __tablename__ = "regulations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    region: Mapped[str] = mapped_column(String(100), nullable=False)
    species_id: Mapped[int] = mapped_column(ForeignKey("fish_species.id"), nullable=False)
    min_length: Mapped[int] = mapped_column(Integer, nullable=False)
    banned_period: Mapped[str] = mapped_column(String(100), nullable=False)
    fine: Mapped[str] = mapped_column(String(50), nullable=False)

    species = relationship("FishSpecies", back_populates="regulations")
