from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)

class UserPublic(BaseModel):
    id: int
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr

class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)
    expires_at: datetime
    topic_ids: list[int] = Field(min_length=1)

class ReactionCreate(BaseModel):
    reaction: str = Field(min_length=1, max_length=50)

class CommentCreate(BaseModel):
    body: str = Field(min_length=1)

class TopicPublic(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)

class CommentPublic(BaseModel):
    id: int
    post_id: int
    user_id: int
    body: str = Field(min_length=1)
    created_at: datetime

class PostPublic(BaseModel):
    id: int
    author_id: int
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)
    created_at: datetime
    expires_at: datetime
    topics: list[TopicPublic]