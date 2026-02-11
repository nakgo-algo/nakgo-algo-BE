from pydantic import BaseModel


class ErrorResponse(BaseModel):
    message: str
    code: str


class SuccessResponse(BaseModel):
    success: bool
