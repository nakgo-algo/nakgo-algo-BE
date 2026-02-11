from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Zone
from app.schemas.zone import ZoneResponse

router = APIRouter(prefix="/zones", tags=["zones"])


@router.get("", response_model=list[ZoneResponse])
def list_zones(db: Session = Depends(get_db)):
    rows = db.query(Zone).order_by(Zone.id.asc()).all()
    return [
        ZoneResponse(
            id=row.id,
            name=row.name,
            type=row.type,
            coordinates=row.coordinates,
            description=row.description,
            period=row.period,
        )
        for row in rows
    ]
