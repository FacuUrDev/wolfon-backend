import uuid

from pydantic import BaseModel, Field
from uuid import UUID


class Card(BaseModel):
    model_config = {
        "extra": "allow"  # Allows arbitrary fields
    }
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    user_id: UUID
    name: str


class User(BaseModel):
    model_config = {
        "extra": "allow"  # Allows arbitrary fields
    }
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    email: str
