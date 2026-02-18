from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from dependencies import handle_session
from models import Post, Tag
from schemas import PostCreateSchema
import schemas

blog_router = APIRouter(prefix="/blog", dependencies=[Depends(handle_session)])

# CREATING POSTS


@blog_router.post(
    "/posts",
    response_model=schemas.PostResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post_data: PostCreateSchema,
    session: Session = Depends(handle_session),
):
    db_tags = []

    for tag_name in post_data.tags:
        tag = session.query(Tag).filter(Tag.name == tag_name).first()

        if not tag:
            tag = Tag(name=tag_name)
        db_tags.append(tag)

    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        category=post_data.category,
        tags=db_tags,
    )

    try:
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post
    except:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error trying to create a new post.",
        )


# LISTING POSTS


@blog_router.get(
    "/posts",
    response_model=list[schemas.PostResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_posts(term: str = None, session: Session = Depends(handle_session)):
    query = session.query(Post)

    if term:
        search_pattern = f"%{term}%"

        query = query.filter(
            or_(
                Post.title.ilike(search_pattern),
                Post.content.ilike(search_pattern),
                Post.category.ilike(search_pattern),
            )
        )

    posts = query.all()

    if len(posts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Posts containing the paramenter '{term}' were not found.",
        )

    return posts


@blog_router.get(
    "/posts/{post_id}",
    response_model=schemas.PostResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_post_by_id(post_id: int, session: Session = Depends(handle_session)):
    post = session.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found."
        )
    return post


# UPDATING POSTS
@blog_router.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    post_data: PostCreateSchema,
    session: Session = Depends(handle_session),
):
    post = session.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found."
        )

    post.title = post_data.title
    post.content = post_data.content
    post.category = post_data.category

    new_tags = []

    for tag_name in post_data.tags:
        tag = session.query(Tag).filter(Tag.name == tag_name).first()

        if not tag:
            tag = Tag(name=tag_name)
        new_tags.append(tag)

    post.tags = new_tags

    try:
        session.commit()
        session.refresh(post)
        return post
    except:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error trying to update the post.",
        )


# DELETING POSTS
@blog_router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    session: Session = Depends(handle_session),
):

    post = session.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog post not found."
        )

    try:
        session.delete(post)
        session.commit()
        return None
    except:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error trying to delete the post.",
        )
