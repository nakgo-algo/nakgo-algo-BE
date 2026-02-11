from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.core.middleware import GlobalRateLimitMiddleware, RequestSizeLimitMiddleware, SecurityHeadersMiddleware
from app.routers import auth, fish, fines, points, posts, profile, regulations, reports, zones
from app.services.seed import seed_reference_data
from app.services.token_service import cleanup_expired_tokens


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_reference_data(db)
        cleanup_expired_tokens(db)
    finally:
        db.close()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
app.add_middleware(GlobalRateLimitMiddleware)
app.add_middleware(RequestSizeLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and {"message", "code"}.issubset(exc.detail.keys()):
        body = exc.detail
    else:
        body = {"message": str(exc.detail), "code": "HTTP_ERROR"}
    return JSONResponse(status_code=exc.status_code, content=body)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    message = exc.errors()[0].get("msg", "잘못된 요청입니다.") if exc.errors() else "잘못된 요청입니다."
    return JSONResponse(status_code=400, content={"message": message, "code": "VALIDATION_ERROR"})


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    logger.exception("Unhandled server error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"message": "서버 내부 오류가 발생했습니다.", "code": "INTERNAL_SERVER_ERROR"},
    )


app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(profile.router, prefix=settings.api_prefix)
app.include_router(fish.router, prefix=settings.api_prefix)
app.include_router(regulations.router, prefix=settings.api_prefix)
app.include_router(fines.router, prefix=settings.api_prefix)
app.include_router(points.router, prefix=settings.api_prefix)
app.include_router(posts.router, prefix=settings.api_prefix)
app.include_router(reports.router, prefix=settings.api_prefix)
app.include_router(zones.router, prefix=settings.api_prefix)
