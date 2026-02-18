from sqlalchemy import (
    Table,
    create_engine,
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from sqlalchemy.sql import func

db = create_engine("sqlite:///database.db")

Base = declarative_base()

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Post(Base):
    __tablename__ = "posts"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=False)
    content = Column("content", String, nullable=False)
    category = Column("category", String, nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )

    tags = relationship("Tag", secondary=post_tags, back_populates="posts")


class Tag(Base):
    __tablename__ = "tags"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")
