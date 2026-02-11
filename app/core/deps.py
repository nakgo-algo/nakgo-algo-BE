from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import unauthorized
from app.core.security import decode_token
from app.models import TokenBlocklist, User


bearer_scheme = HTTPBearer(auto_error=True)


def _is_token_blocked(db: Session, token: str) -> bool:
    return db.query(TokenBlocklist).filter(TokenBlocklist.token == token).first() is not None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    if _is_token_blocked(db, token):
        raise unauthorized("만료되었거나 로그아웃된 토큰입니다.", "TOKEN_BLOCKED")

    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub", "0"))
    except (ValueError, TypeError):
        raise unauthorized("유효하지 않은 토큰입니다.", "INVALID_TOKEN")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise unauthorized("사용자를 찾을 수 없습니다.", "USER_NOT_FOUND")

    return user


def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    return credentials.credentials
