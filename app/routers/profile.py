from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.schemas.profile import UpdateNicknameRequest
from app.schemas.user import UserPublic

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=UserPublic)
def get_profile(current_user: User = Depends(get_current_user)):
    return UserPublic.model_validate(current_user)


@router.put("/nickname", response_model=UserPublic)
def update_nickname(
    payload: UpdateNicknameRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.nickname = payload.nickname
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return UserPublic.model_validate(current_user)
