from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, UniqueConstraint

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    username = Column(String, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

posts_topics = Table(
    "posts_topics",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("topic_id", Integer, ForeignKey("topics.id"), primary_key=True)
)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    title = Column(String, nullable=False)

    body = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False)

    expires_at = Column(DateTime, nullable=False)

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, unique=True, nullable=False)

class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    reaction = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("post_id", "user_id"),
    )

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    body = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False)