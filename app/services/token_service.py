import hashlib
import secrets
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import RefreshToken, TokenBlocklist


def create_refresh_token(db: Session, user_id: int) -> str:
    raw_token = secrets.token_urlsafe(48)
    token_hash = hash_token(raw_token)
    expires_at = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)

    db.add(RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at))
    db.commit()
    return raw_token


def rotate_refresh_token(db: Session, raw_token: str) -> RefreshToken | None:
    token_hash = hash_token(raw_token)
    row = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    if not row:
        return None

    now = datetime.utcnow()
    if row.revoked_at is not None or row.expires_at < now:
        return None

    row.revoked_at = now
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def revoke_refresh_token(db: Session, raw_token: str) -> bool:
    token_hash = hash_token(raw_token)
    row = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    if not row or row.revoked_at is not None:
        return False

    row.revoked_at = datetime.utcnow()
    db.add(row)
    db.commit()
    return True


def cleanup_expired_tokens(db: Session) -> None:
    now = datetime.utcnow()
    db.query(TokenBlocklist).filter(TokenBlocklist.expires_at < now).delete(synchronize_session=False)
    db.query(RefreshToken).filter(RefreshToken.expires_at < now).delete(synchronize_session=False)
    db.commit()


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
