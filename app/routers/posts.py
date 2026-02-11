from fastapi import APIRouter, Depends
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.errors import forbidden, not_found
from app.models import Comment, Post, User
from app.schemas.common import SuccessResponse
from app.schemas.post import (
    CommentCreateRequest,
    CommentItem,
    PostCreateRequest,
    PostDetailResponse,
    PostListItem,
)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=list[PostListItem])
def list_posts(search: str | None = None, db: Session = Depends(get_db)):
    comment_count_subquery = (
        db.query(Comment.post_id, func.count(Comment.id).label("comment_count"))
        .group_by(Comment.post_id)
        .subquery()
    )

    query = (
        db.query(Post, User.nickname, func.coalesce(comment_count_subquery.c.comment_count, 0))
        .join(User, Post.user_id == User.id)
        .outerjoin(comment_count_subquery, Post.id == comment_count_subquery.c.post_id)
        .order_by(Post.created_at.desc())
    )
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Post.title.like(like), Post.content.like(like)))

    rows = query.all()
    return [
        PostListItem(
            id=post.id,
            title=post.title,
            content=post.content,
            author=nickname,
            date=post.created_at.strftime("%Y-%m-%d"),
            comments=comment_count,
            image=post.image,
        )
        for post, nickname, comment_count in rows
    ]


@router.post("", response_model=PostListItem, status_code=201)
def create_post(
    payload: PostCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = Post(user_id=current_user.id, title=payload.title, content=payload.content)
    db.add(row)
    db.commit()
    db.refresh(row)

    return PostListItem(
        id=row.id,
        title=row.title,
        content=row.content,
        author=current_user.nickname,
        date=row.created_at.strftime("%Y-%m-%d"),
        comments=0,
        image=row.image,
    )


@router.get("/{post_id}", response_model=PostDetailResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise not_found("게시글을 찾을 수 없습니다.", "POST_NOT_FOUND")

    comments = (
        db.query(Comment, User.nickname)
        .join(User, Comment.user_id == User.id)
        .filter(Comment.post_id == post.id)
        .order_by(Comment.created_at.asc())
        .all()
    )
    return PostDetailResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author=post.user.nickname,
        date=post.created_at.strftime("%Y-%m-%d"),
        comments=[
            CommentItem(
                id=comment.id,
                text=comment.text,
                author=nickname,
                date=comment.created_at.strftime("%Y-%m-%d"),
            )
            for comment, nickname in comments
        ],
    )


@router.delete("/{post_id}", response_model=SuccessResponse)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise not_found("게시글을 찾을 수 없습니다.", "POST_NOT_FOUND")
    if post.user_id != current_user.id:
        raise forbidden("본인 게시글만 삭제할 수 있습니다.", "POST_DELETE_FORBIDDEN")

    db.delete(post)
    db.commit()
    return SuccessResponse(success=True)


@router.get("/{post_id}/comments", response_model=list[CommentItem])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise not_found("게시글을 찾을 수 없습니다.", "POST_NOT_FOUND")

    rows = (
        db.query(Comment, User.nickname)
        .join(User, Comment.user_id == User.id)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
        .all()
    )
    return [
        CommentItem(
            id=comment.id,
            text=comment.text,
            author=nickname,
            date=comment.created_at.strftime("%Y-%m-%d"),
        )
        for comment, nickname in rows
    ]


@router.post("/{post_id}/comments", response_model=CommentItem, status_code=201)
def create_comment(
    post_id: int,
    payload: CommentCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise not_found("게시글을 찾을 수 없습니다.", "POST_NOT_FOUND")

    row = Comment(post_id=post_id, user_id=current_user.id, text=payload.text)
    db.add(row)
    db.commit()
    db.refresh(row)
    return CommentItem(
        id=row.id,
        text=row.text,
        author=current_user.nickname,
        date=row.created_at.strftime("%Y-%m-%d"),
    )
