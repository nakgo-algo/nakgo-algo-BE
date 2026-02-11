from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Fine(Base):
    __tablename__ = "fines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    species: Mapped[str] = mapped_column(String(100), nullable=False)
    violation: Mapped[str] = mapped_column(String(100), nullable=False)
    fine_amount: Mapped[str] = mapped_column(String(50), nullable=False)
    legal_basis: Mapped[str] = mapped_column(String(255), nullable=False)
