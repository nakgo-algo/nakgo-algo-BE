import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.errors import forbidden, not_found
from app.models import Notification, Post, User
from app.models.moderation import ModerationRequest
from app.schemas.common import SuccessResponse
from app.schemas.moderation import ModerationListItem, ModerationResolveRequest

router = APIRouter(prefix="/moderation", tags=["moderation"])


@router.get("", response_model=list[ModerationListItem])
def list_moderation(
    status: str = "pending",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin":
        raise forbidden("관리자 권한이 필요합니다.", "ADMIN_REQUIRED")

    rows = (
        db.query(ModerationRequest, Post.title, Post.content, User.nickname)
        .join(Post, ModerationRequest.post_id == Post.id)
        .join(User, Post.user_id == User.id)
        .filter(ModerationRequest.status == status)
        .order_by(ModerationRequest.created_at.desc())
        .all()
    )

    return [
        ModerationListItem(
            id=mr.id,
            postTitle=title,
            postContent=content,
            postAuthor=nickname,
            reason=mr.reason,
            matchedWords=json.loads(mr.matched_words),
            createdAt=mr.created_at,
        )
        for mr, title, content, nickname in rows
    ]


@router.put("/{moderation_id}/resolve", response_model=SuccessResponse)
def resolve_moderation(
    moderation_id: int,
    payload: ModerationResolveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin":
        raise forbidden("관리자 권한이 필요합니다.", "ADMIN_REQUIRED")

    mr = db.query(ModerationRequest).filter(ModerationRequest.id == moderation_id).first()
    if not mr:
        raise not_found("검토 요청을 찾을 수 없습니다.", "MODERATION_NOT_FOUND")

    mr.status = "resolved"
    mr.resolved_action = payload.action

    if payload.action == "delete":
        post = db.query(Post).filter(Post.id == mr.post_id).first()
        if post:
            notification = Notification(
                user_id=post.user_id,
                type="post_deleted",
                title="게시글이 삭제되었습니다",
                message=f"'{post.title}' 게시글이 관리자에 의해 삭제되었습니다. 사유: {payload.deleteReason or '부적절한 내용'}",
            )
            db.add(notification)
            db.delete(post)

    db.commit()
    return SuccessResponse(success=True)
