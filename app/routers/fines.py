from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Fine
from app.schemas.fine import FineResponse

router = APIRouter(prefix="/fines", tags=["fines"])


@router.get("", response_model=list[FineResponse])
def list_fines(db: Session = Depends(get_db)):
    rows = db.query(Fine).order_by(Fine.id.asc()).all()
    return [
        FineResponse(
            id=row.id,
            species=row.species,
            violation=row.violation,
            fineAmount=row.fine_amount,
            legalBasis=row.legal_basis,
        )
        for row in rows
    ]
