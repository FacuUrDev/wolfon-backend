from datetime import datetime, UTC
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Card(BaseModel):
    title: Optional[str]
    user_id: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}
        extra = "allow"


class User(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None
    name: str
    email: str

    class Config:
        json_encoders = {ObjectId: str}
        extra = "allow"
