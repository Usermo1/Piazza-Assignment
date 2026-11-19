from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from security import get_current_user

router = APIRouter()


def _post_public(post: models.Post, topics: list[schemas.TopicPublic]) -> schemas.PostPublic:
    return schemas.PostPublic(
        id=post.id,
        author_id=post.author_id,
        title=post.title,
        body=post.body,
        created_at=post.created_at,
        expires_at=post.expires_at,
        topics=topics,
    )


def _posts_public(db: Session, posts: list[models.Post]) -> list[schemas.PostPublic]:
    if not posts:
        return []

    topics_by_post = {post.id: [] for post in posts}
    topic_rows = (
        db.query(models.posts_topics.c.post_id, models.Topic)
        .join(models.Topic, models.Topic.id == models.posts_topics.c.topic_id)
        .filter(models.posts_topics.c.post_id.in_(topics_by_post))
        .all()
    )
    for post_id, topic in topic_rows:
        topics_by_post[post_id].append(
            schemas.TopicPublic(id=topic.id, name=topic.name)
        )

    return [
        _post_public(post, topics_by_post[post.id])
        for post in posts
    ]


@router.post("/", response_model=schemas.PostPublic, status_code=201)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    created_at = datetime.now(timezone.utc)

    if post.expires_at <= created_at:
        raise HTTPException(status_code=400, detail="Expiry time must be in the future")

    if len(post.topic_ids) != len(set(post.topic_ids)):
        raise HTTPException(status_code=400, detail="Duplicate topic IDs are not allowed")
    
    topics = []
    for topic_id in post.topic_ids:
        topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
        if topic is None:
            raise HTTPException(status_code=400, detail="Invalid topic ID")
        topics.append(schemas.TopicPublic(id=topic.id, name=topic.name))

    db_post = models.Post(
        author_id=current_user.id,
        title=post.title,
        body=post.body,
        created_at=created_at,
        expires_at=post.expires_at
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    for topic_id in post.topic_ids:
        db.execute(models.posts_topics.insert().values(post_id=db_post.id, topic_id=topic_id))
    db.commit()

    return _post_public(db_post, topics)

@router.get("/", response_model=list[schemas.PostPublic])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return _posts_public(db, posts)

@router.get("/{post_id}", response_model=schemas.PostPublic)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return _posts_public(db, [post])[0]
    