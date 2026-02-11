from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from threading import Lock

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(self)"
        response.headers["X-XSS-Protection"] = "0"
        return response


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                if int(content_length) > settings.max_request_size_bytes:
                    return JSONResponse(
                        status_code=413,
                        content={"message": "요청 본문이 너무 큽니다.", "code": "REQUEST_TOO_LARGE"},
                    )
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"message": "잘못된 Content-Length 값입니다.", "code": "INVALID_CONTENT_LENGTH"},
                )

        return await call_next(request)


class GlobalRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.lock = Lock()
        self.window_seconds = 60
        self.limit_per_window = settings.global_rate_limit_per_minute
        self.request_history: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        client_ip = _get_client_ip(request)
        now = datetime.now(timezone.utc).timestamp()
        cutoff = now - self.window_seconds

        with self.lock:
            history = self.request_history[client_ip]
            while history and history[0] <= cutoff:
                history.popleft()

            if len(history) >= self.limit_per_window:
                retry_after = int(max(1, self.window_seconds - (now - history[0])))
                return JSONResponse(
                    status_code=429,
                    content={"message": "요청이 너무 많습니다. 잠시 후 다시 시도해주세요.", "code": "RATE_LIMITED"},
                    headers={"Retry-After": str(retry_after)},
                )

            history.append(now)

        return await call_next(request)


def _get_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


class KakaoLoginGuard:
    def __init__(self):
        self.lock = Lock()
        self.failures: dict[str, deque[float]] = defaultdict(deque)
        self.blocked_until: dict[str, float] = {}

    def assert_allowed(self, ip: str) -> None:
        now = datetime.now(timezone.utc).timestamp()
        with self.lock:
            blocked_until = self.blocked_until.get(ip)
            if blocked_until and now < blocked_until:
                raise PermissionError("TOO_MANY_LOGIN_FAILURES")
            if blocked_until and now >= blocked_until:
                self.blocked_until.pop(ip, None)

    def record_failure(self, ip: str) -> None:
        now = datetime.now(timezone.utc).timestamp()
        cutoff = now - 300
        with self.lock:
            bucket = self.failures[ip]
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()
            bucket.append(now)

            if len(bucket) >= settings.kakao_login_max_attempts:
                blocked_until = datetime.now(timezone.utc) + timedelta(minutes=settings.kakao_login_block_minutes)
                self.blocked_until[ip] = blocked_until.timestamp()
                self.failures[ip].clear()

    def record_success(self, ip: str) -> None:
        with self.lock:
            self.failures.pop(ip, None)
            self.blocked_until.pop(ip, None)


kakao_login_guard = KakaoLoginGuard()
