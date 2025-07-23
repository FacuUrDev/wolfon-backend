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
