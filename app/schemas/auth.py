from pydantic import BaseModel

from app.schemas.user import UserPublic


class KakaoLoginRequest(BaseModel):
    accessToken: str


class AuthResponse(BaseModel):
    token: str
    user: UserPublic


class VerifyResponse(BaseModel):
    valid: bool
    user: UserPublic
