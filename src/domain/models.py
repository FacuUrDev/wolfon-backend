from datetime import datetime, UTC
from typing import Optional, Any

from bson import ObjectId
from pydantic import BaseModel, Field


class Card(BaseModel):
    id: Optional[Any] = Field(default_factory=lambda: str(ObjectId()))
    title: Optional[str]
    user_id: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}
        extra = "allow"
        arbitrary_types_allowed = True


class User(BaseModel):
    id: Optional[Any] = Field(default_factory=lambda: str(ObjectId()))
    name: str
    email: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}
        extra = "allow"
        arbitrary_types_allowed = True
# test_card = {
#     "_id": ObjectId("686ef1855ccdea898607335a"),
#   "user_id": "686ef1855ccdea898607335b",
#   "title": "Test Card"
# }
# Card.model_validate(test_card)
