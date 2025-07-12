from datetime import datetime, UTC
from typing import Optional, Any, Annotated

from bson import ObjectId
from pydantic import BaseModel, Field, model_serializer
from pydantic_mongo import ObjectIdAnnotation

ObjectIdCustom = Annotated[
    Any, lambda x: ObjectId(x) if isinstance(x, str) else x
]


class Card(BaseModel):
    id: Optional[ObjectIdCustom] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    title: Optional[str]
    user_id: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    class Config:
        extra = "allow"
        arbitrary_types_allowed = True

    @model_serializer()
    def serialize(self):
        self.__dict__["_id"] = self.id
        return self.__dict__


class User(BaseModel):
    id: ObjectIdAnnotation = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    email: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    class Config:
        extra = "allow"
        arbitrary_types_allowed = True

    @model_serializer()
    def serialize(self):
        self.__dict__["_id"] = self.id
        return self.__dict__

# test_card = {
#     "_id": ObjectId("686ef1855ccdea898607335a"),
#   "user_id": "686ef1855ccdea898607335b",
#   "title": "Test Card"
# }
# Card.model_validate(test_card)
