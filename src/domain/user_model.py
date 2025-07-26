from typing import Any, Annotated, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from src.domain.subscription_model import Subscription

ObjectIdCustom = Annotated[
    Any, lambda x: ObjectId(x) if isinstance(x, str) else x
]


class User(BaseModel):
    name: str
    email: str
    subscription: Optional[Subscription] = Field(..., description="Subscription of the user")

    class Config:
        extra = "allow"
        arbitrary_types_allowed = True
