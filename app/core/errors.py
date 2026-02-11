from fastapi import HTTPException, status


def api_error(status_code: int, message: str, code: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"message": message, "code": code})


def bad_request(message: str, code: str = "BAD_REQUEST") -> HTTPException:
    return api_error(status.HTTP_400_BAD_REQUEST, message, code)


def unauthorized(message: str = "인증이 필요합니다.", code: str = "UNAUTHORIZED") -> HTTPException:
    return api_error(status.HTTP_401_UNAUTHORIZED, message, code)


def forbidden(message: str = "권한이 없습니다.", code: str = "FORBIDDEN") -> HTTPException:
    return api_error(status.HTTP_403_FORBIDDEN, message, code)


def not_found(message: str = "리소스를 찾을 수 없습니다.", code: str = "NOT_FOUND") -> HTTPException:
    return api_error(status.HTTP_404_NOT_FOUND, message, code)
