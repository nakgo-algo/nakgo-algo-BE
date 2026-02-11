from pydantic import BaseModel, Field


class ReportCreateRequest(BaseModel):
    type: str = Field(pattern="^(missing|wrong|boundary|other)$")
    title: str = Field(min_length=1, max_length=200)
    location: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)


class ReportListItem(BaseModel):
    id: int
    type: str
    title: str
    location: str
    description: str
    status: str
    author: str
    createdAt: str


class ReportCreateResponse(BaseModel):
    id: int
    type: str
    title: str
    status: str
    createdAt: str
