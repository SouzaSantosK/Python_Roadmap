from typing import List
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime


class TagSchema(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class PostCreateSchema(BaseModel):
    title: str = Field(
        ..., min_length=1, json_schema_extra={"example": "My First Post"}
    )
    content: str = Field(
        ..., min_length=1, json_schema_extra={"example": "Write about your post here"}
    )
    category: str = Field(..., json_schema_extra={"example": "Tech"})
    tags: List[str] = Field(..., json_schema_extra={"example": ["Tech", "Programming"]})

    model_config = ConfigDict(from_attributes=True)


class PostResponseSchema(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: List[str]
    createdAt: datetime
    updatedAt: datetime

    model_config = ConfigDict(from_attributes=True)

    # pre-processor
    @field_validator("tags", mode="before")
    @classmethod
    def transform_tags(cls, v):
        if isinstance(v, list) and v and not isinstance(v[0], str):
            return [tag.name for tag in v]
        return v
