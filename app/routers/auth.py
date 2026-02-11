from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_token, get_current_user
from app.core.errors import bad_request, unauthorized
from app.core.security import create_access_token, decode_token
from app.models import TokenBlocklist, User
from app.schemas.auth import AuthResponse, KakaoLoginRequest, VerifyResponse
from app.schemas.common import SuccessResponse
from app.schemas.user import UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


async def _fetch_kakao_user(access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient(timeout=8.0) as client:
        response = await client.get("https://kapi.kakao.com/v2/user/me", headers=headers)
    if response.status_code != 200:
        raise unauthorized("카카오 토큰이 유효하지 않습니다.", "KAKAO_AUTH_FAILED")
    return response.json()


@router.post("/kakao", response_model=AuthResponse)
async def kakao_login(payload: KakaoLoginRequest, db: Session = Depends(get_db)):
    kakao_user = await _fetch_kakao_user(payload.accessToken)

    kakao_id = str(kakao_user.get("id", ""))
    if not kakao_id:
        raise bad_request("카카오 사용자 정보를 가져오지 못했습니다.", "KAKAO_USER_INFO_INVALID")

    account = kakao_user.get("kakao_account", {})
    properties = kakao_user.get("properties", {})

    email = account.get("email")
    nickname = properties.get("nickname") or f"kakao_{kakao_id[-6:]}"
    profile_image = properties.get("profile_image")

    user = db.query(User).filter(User.kakao_id == kakao_id).first()
    if not user:
        user = User(kakao_id=kakao_id, email=email, nickname=nickname, profile_image=profile_image)
        db.add(user)
    else:
        user.email = email
        user.nickname = nickname
        user.profile_image = profile_image

    db.commit()
    db.refresh(user)

    token = create_access_token(subject=str(user.id))
    return AuthResponse(token=token, user=UserPublic.model_validate(user))


@router.get("/verify", response_model=VerifyResponse)
def verify_token(current_user: User = Depends(get_current_user)):
    return VerifyResponse(valid=True, user=UserPublic.model_validate(current_user))


@router.post("/logout", response_model=SuccessResponse)
def logout(
    token: str = Depends(get_current_token),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_token(token)
    except ValueError:
        raise unauthorized("유효하지 않은 토큰입니다.", "INVALID_TOKEN")
    exp = payload.get("exp")
    if exp is None:
        raise unauthorized("유효하지 않은 토큰입니다.", "INVALID_TOKEN")

    expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
    exists = db.query(TokenBlocklist).filter(TokenBlocklist.token == token).first()
    if not exists:
        db.add(TokenBlocklist(token=token, expires_at=expires_at))
        db.commit()

    return SuccessResponse(success=True)
