from datetime import datetime, UTC
from enum import Enum
from typing import Any, Annotated, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

ObjectIdCustom = Annotated[
    Any, lambda x: ObjectId(x) if isinstance(x, str) else x
]


class SubscriptionStatus(str, Enum):
    active = "active"
    expired = "expired"
    cancelled = "cancelled"
    pending = "pending"


class SubscriptionState(BaseModel):
    active: bool = True
    valid_from: datetime
    valid_to: datetime = None
    status: SubscriptionStatus = SubscriptionStatus.active



class Subscription(BaseModel):
    tier: str = Field("free", description="Tier of the subscription, e.g., free, premium, enterprise")
    name: Optional[str] = None
    display_name: str = Field(None, description="Display name of the subscription")
    price: float = None
    currency: str = "USD"
    features: list[str] = []
    state: SubscriptionState = Field(..., description="State of the subscription")


if __name__ == '__main__':
    from src.infrastructure import get_database
    from pprint import pp

    db = get_database("wolfon_dev")
    subs = list(db.subscriptions.find({}))
    sub = Subscription(**subs[0])
    pp(sub.model_dump(exclude={"_id"}))
    print(sub.model_dump_json(exclude={"_id"}))
