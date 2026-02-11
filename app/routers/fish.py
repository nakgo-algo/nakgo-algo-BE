import hashlib
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import not_found
from app.models import FishSpecies
from app.schemas.fish import (
    FishAnalyzeRequest,
    FishAnalyzeResponse,
    FishCheckRequest,
    FishCheckResponse,
    FishRegulationInfo,
    FishSpeciesItem,
)

router = APIRouter(prefix="/fish", tags=["fish"])


def _build_regulation_description(min_length: int, banned_months: list[int]) -> str:
    if not banned_months:
        return f"최소 체장 {min_length}cm"
    sorted_months = sorted(set(banned_months))
    month_text = ", ".join(str(month) for month in sorted_months)
    return f"최소 체장 {min_length}cm, 금어기 {month_text}월"


@router.post("/analyze", response_model=FishAnalyzeResponse)
def analyze_fish(payload: FishAnalyzeRequest, db: Session = Depends(get_db)):
    species_rows = db.query(FishSpecies).order_by(FishSpecies.id.asc()).all()
    if not species_rows:
        raise not_found("어종 데이터가 없습니다.", "FISH_SPECIES_NOT_FOUND")

    digest = hashlib.sha256(payload.image.encode("utf-8")).hexdigest()
    index = int(digest[:8], 16) % len(species_rows)
    selected = species_rows[index]

    confidence = 0.75 + ((int(digest[8:10], 16) % 20) / 100)
    regulation = FishRegulationInfo(
        minLength=selected.min_length,
        bannedMonths=selected.banned_months,
        description=_build_regulation_description(selected.min_length, selected.banned_months),
    )
    return FishAnalyzeResponse(species=selected.name, confidence=round(confidence, 2), regulation=regulation)


@router.get("/species", response_model=list[FishSpeciesItem])
def list_species(db: Session = Depends(get_db)):
    rows = db.query(FishSpecies).order_by(FishSpecies.id.asc()).all()
    return [
        FishSpeciesItem(
            name=row.name,
            minLength=row.min_length,
            bannedMonths=row.banned_months,
            category=row.category,
        )
        for row in rows
    ]


@router.post("/check", response_model=FishCheckResponse)
def check_fish(payload: FishCheckRequest, db: Session = Depends(get_db)):
    species = db.query(FishSpecies).filter(FishSpecies.name == payload.species).first()
    if not species:
        raise not_found("해당 어종을 찾을 수 없습니다.", "SPECIES_NOT_FOUND")

    current_month = datetime.utcnow().month
    is_under_size = payload.length < species.min_length
    is_banned_period = current_month in (species.banned_months or [])

    if is_under_size:
        message = f"최소 체장({species.min_length}cm) 미달입니다. 방류해주세요."
    elif is_banned_period:
        message = "현재 금어기입니다. 방류해주세요."
    else:
        message = "규정 위반이 아닙니다."

    return FishCheckResponse(
        species=species.name,
        inputLength=payload.length,
        minLength=species.min_length,
        isUnderSize=is_under_size,
        isBannedPeriod=is_banned_period,
        message=message,
    )
