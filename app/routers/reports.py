from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import Report, User
from app.schemas.report import ReportCreateRequest, ReportCreateResponse, ReportListItem

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=list[ReportListItem])
def list_reports(
    status: str | None = None,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Report, User.nickname).join(User, Report.user_id == User.id)
    if status:
        query = query.filter(Report.status == status)
    rows = query.order_by(Report.created_at.desc()).all()

    return [
        ReportListItem(
            id=report.id,
            type=report.type,
            title=report.title,
            location=report.location,
            description=report.description,
            status=report.status,
            author=nickname,
            createdAt=report.created_at.strftime("%Y-%m-%d"),
        )
        for report, nickname in rows
    ]


@router.post("", response_model=ReportCreateResponse, status_code=201)
def create_report(
    payload: ReportCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = Report(
        user_id=current_user.id,
        type=payload.type,
        title=payload.title,
        location=payload.location,
        description=payload.description,
        status="pending",
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return ReportCreateResponse(
        id=row.id,
        type=row.type,
        title=row.title,
        status=row.status,
        createdAt=row.created_at.strftime("%Y-%m-%d"),
    )
