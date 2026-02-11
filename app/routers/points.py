from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.errors import not_found
from app.models import Point, User
from app.schemas.common import SuccessResponse
from app.schemas.point import PointCreateRequest, PointResponse

router = APIRouter(prefix="/points", tags=["points"])


@router.get("", response_model=list[PointResponse])
def list_points(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Point).filter(Point.user_id == current_user.id).order_by(Point.created_at.desc()).all()
    return [
        PointResponse(
            id=row.id,
            name=row.name,
            lat=row.lat,
            lng=row.lng,
            memo=row.memo,
            color=row.color,
            createdAt=row.created_at,
        )
        for row in rows
    ]


@router.post("", response_model=PointResponse, status_code=201)
def create_point(
    payload: PointCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = Point(
        user_id=current_user.id,
        name=payload.name,
        lat=payload.lat,
        lng=payload.lng,
        memo=payload.memo,
        color=payload.color,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return PointResponse(
        id=row.id,
        name=row.name,
        lat=row.lat,
        lng=row.lng,
        memo=row.memo,
        color=row.color,
        createdAt=row.created_at,
    )


@router.delete("/{point_id}", response_model=SuccessResponse)
def delete_point(
    point_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = db.query(Point).filter(Point.id == point_id, Point.user_id == current_user.id).first()
    if not row:
        raise not_found("포인트를 찾을 수 없습니다.", "POINT_NOT_FOUND")

    db.delete(row)
    db.commit()
    return SuccessResponse(success=True)
