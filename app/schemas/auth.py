from pydantic import BaseModel

from app.schemas.user import UserPublic


class KakaoLoginRequest(BaseModel):
    accessToken: str


class AuthResponse(BaseModel):
    token: str
    refreshToken: str
    user: UserPublic


class RefreshRequest(BaseModel):
    refreshToken: str


class RefreshResponse(BaseModel):
    token: str
    refreshToken: str


class VerifyResponse(BaseModel):
    valid: bool
    user: UserPublic


class LogoutRequest(BaseModel):
    refreshToken: str | None = None
