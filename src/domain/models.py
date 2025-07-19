from typing import Optional, Any, Annotated

from bson import ObjectId
from pydantic import BaseModel

ObjectIdCustom = Annotated[
    Any, lambda x: ObjectId(x) if isinstance(x, str) else x
]


class Card(BaseModel):
    user_id: str
    title: Optional[str]

    class Config:
        extra = "allow"
        arbitrary_types_allowed = True


class User(BaseModel):
    name: str
    email: str

    class Config:
        extra = "allow"
        arbitrary_types_allowed = True


if __name__ == "__main__":
    test_card = {
        "_id": ObjectId("686ef1855ccdea898607335a"),
        "user_id": "686ef1855ccdea898607335b",
        "title": "Test Card"
    }

    test2_card = {
        "id": ObjectId("6875e184163cee43620fdca7"),
        "title": "Tarjeta de facu tocada"
    }
    Card.model_validate(test_card)
    Card.model_validate(test2_card)
