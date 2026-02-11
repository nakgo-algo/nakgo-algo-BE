from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "NakgoAlgo API"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./nakgo_algo.db"
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    cors_allow_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    cors_allow_credentials: bool = True

    max_request_size_bytes: int = 5 * 1024 * 1024
    global_rate_limit_per_minute: int = 120
    kakao_login_max_attempts: int = 8
    kakao_login_block_minutes: int = 10

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret_key(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("JWT_SECRET_KEY must be set and at least 32 chars")
        return value


settings = Settings()
