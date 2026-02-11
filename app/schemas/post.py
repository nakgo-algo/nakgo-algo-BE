from pydantic import BaseModel, Field


class PostCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class PostListItem(BaseModel):
    id: int
    title: str
    content: str
    author: str
    date: str
    comments: int
    image: str | None = None


class CommentItem(BaseModel):
    id: int
    text: str
    author: str
    date: str


class PostDetailResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    date: str
    comments: list[CommentItem]


class CommentCreateRequest(BaseModel):
    text: str = Field(min_length=1)
