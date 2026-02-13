from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import Notification, User
from app.schemas.common import SuccessResponse
from app.schemas.notification import NotificationOut, UnreadCountResponse

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/unread-count", response_model=UnreadCountResponse)
def get_unread_count(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read.is_(False),
    ).count()
    return UnreadCountResponse(count=count)


@router.get("", response_model=list[NotificationOut])
def get_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .limit(50)
        .all()
    )
    return [NotificationOut.from_orm_row(r) for r in rows]


@router.put("/read-all", response_model=SuccessResponse)
def read_all(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read.is_(False),
    ).update({"is_read": True})
    db.commit()
    return SuccessResponse(success=True)
