from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import not_found
from app.models import Regulation
from app.schemas.regulation import RegulationRegionResponse, RegulationSpeciesItem

router = APIRouter(prefix="/regulations", tags=["regulations"])


@router.get("", response_model=list[RegulationRegionResponse])
def list_regulations(db: Session = Depends(get_db)):
    rows = db.query(Regulation).order_by(Regulation.region_id.asc(), Regulation.id.asc()).all()
    grouped: dict[str, RegulationRegionResponse] = {}

    for row in rows:
        if row.region_id not in grouped:
            grouped[row.region_id] = RegulationRegionResponse(id=row.region_id, region=row.region, species=[])
        grouped[row.region_id].species.append(
            RegulationSpeciesItem(
                name=row.species.name,
                minLength=row.min_length,
                bannedPeriod=row.banned_period,
                fine=row.fine,
            )
        )

    return list(grouped.values())


@router.get("/{region_id}", response_model=RegulationRegionResponse)
def get_regulations_by_region(region_id: str, db: Session = Depends(get_db)):
    rows = db.query(Regulation).filter(Regulation.region_id == region_id).order_by(Regulation.id.asc()).all()
    if not rows:
        raise not_found("해당 지역 규제 정보를 찾을 수 없습니다.", "REGION_NOT_FOUND")

    return RegulationRegionResponse(
        id=rows[0].region_id,
        region=rows[0].region,
        species=[
            RegulationSpeciesItem(
                name=row.species.name,
                minLength=row.min_length,
                bannedPeriod=row.banned_period,
                fine=row.fine,
            )
            for row in rows
        ],
    )
