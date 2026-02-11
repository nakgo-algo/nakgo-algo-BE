from datetime import datetime
from typing import cast

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_token, get_current_user
from app.core.errors import bad_request, forbidden, unauthorized
from app.core.middleware import _get_client_ip, kakao_login_guard
from app.core.security import create_access_token, decode_token
from app.models import TokenBlocklist, User
from app.schemas.auth import (
    AuthResponse,
    KakaoLoginRequest,
    LogoutRequest,
    RefreshRequest,
    RefreshResponse,
    VerifyResponse,
)
from app.schemas.common import SuccessResponse
from app.schemas.user import UserPublic
from app.services.token_service import (
    cleanup_expired_tokens,
    create_refresh_token,
    revoke_refresh_token,
    rotate_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _as_optional_str(value: object) -> str | None:
    return value if isinstance(value, str) else None


async def _fetch_kakao_user(access_token: str) -> dict[str, object]:
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient(timeout=8.0) as client:
        response = await client.get("https://kapi.kakao.com/v2/user/me", headers=headers)
    if response.status_code != 200:
        raise unauthorized("카카오 토큰이 유효하지 않습니다.", "KAKAO_AUTH_FAILED")
    return response.json()


@router.post("/kakao", response_model=AuthResponse)
async def kakao_login(payload: KakaoLoginRequest, request: Request, db: Session = Depends(get_db)):
    client_ip = _get_client_ip(request)
    cleanup_expired_tokens(db)
    try:
        kakao_login_guard.assert_allowed(client_ip)
    except PermissionError:
        raise forbidden("로그인 시도가 너무 많습니다. 잠시 후 다시 시도해주세요.", "KAKAO_LOGIN_BLOCKED")

    try:
        kakao_user = await _fetch_kakao_user(payload.accessToken)
    except HTTPException as exc:
        if isinstance(exc.detail, dict) and exc.detail.get("code") == "KAKAO_AUTH_FAILED":
            kakao_login_guard.record_failure(client_ip)
        raise
    except httpx.HTTPError:
        kakao_login_guard.record_failure(client_ip)
        raise unauthorized("카카오 인증 서버 연결에 실패했습니다.", "KAKAO_UPSTREAM_ERROR")

    kakao_id = str(kakao_user.get("id", ""))
    if not kakao_id:
        raise bad_request("카카오 사용자 정보를 가져오지 못했습니다.", "KAKAO_USER_INFO_INVALID")

    account = cast(dict[str, object], kakao_user.get("kakao_account", {}))
    properties = cast(dict[str, object], kakao_user.get("properties", {}))

    email = _as_optional_str(account.get("email"))
    nickname = _as_optional_str(properties.get("nickname")) or f"kakao_{kakao_id[-6:]}"
    profile_image = _as_optional_str(properties.get("profile_image"))

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
    kakao_login_guard.record_success(client_ip)

    token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(db, user.id)
    return AuthResponse(token=token, refreshToken=refresh_token, user=UserPublic.model_validate(user))


@router.post("/refresh", response_model=RefreshResponse)
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    cleanup_expired_tokens(db)
    existing_token = rotate_refresh_token(db, payload.refreshToken)
    if not existing_token:
        raise unauthorized("유효하지 않거나 만료된 refresh token입니다.", "INVALID_REFRESH_TOKEN")

    token = create_access_token(subject=str(existing_token.user_id))
    new_refresh_token = create_refresh_token(db, existing_token.user_id)
    return RefreshResponse(token=token, refreshToken=new_refresh_token)


@router.get("/verify", response_model=VerifyResponse)
def verify_token(current_user: User = Depends(get_current_user)):
    return VerifyResponse(valid=True, user=UserPublic.model_validate(current_user))


@router.post("/logout", response_model=SuccessResponse)
def logout(
    payload: LogoutRequest | None = None,
    token: str = Depends(get_current_token),
    db: Session = Depends(get_db),
):
    cleanup_expired_tokens(db)
    try:
        token_payload = decode_token(token)
    except ValueError:
        raise unauthorized("유효하지 않은 토큰입니다.", "INVALID_TOKEN")
    exp = token_payload.get("exp")
    if exp is None:
        raise unauthorized("유효하지 않은 토큰입니다.", "INVALID_TOKEN")
    try:
        exp_int = int(exp)
    except (TypeError, ValueError):
        raise unauthorized("유효하지 않은 토큰입니다.", "INVALID_TOKEN")

    expires_at = datetime.utcfromtimestamp(exp_int)
    exists = db.query(TokenBlocklist).filter(TokenBlocklist.token == token).first()
    if not exists:
        db.add(TokenBlocklist(token=token, expires_at=expires_at))
        db.commit()

    if payload and payload.refreshToken:
        revoke_refresh_token(db, payload.refreshToken)

    return SuccessResponse(success=True)
