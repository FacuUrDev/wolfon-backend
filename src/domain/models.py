from datetime import datetime, UTC
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Card(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    title: Optional[str]
    user_id: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}
        extra = "allow"
        arbitrary_types_allowed = True

class User(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    name: str
    email: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}
        extra = "allow"
        arbitrary_types_allowed = True
