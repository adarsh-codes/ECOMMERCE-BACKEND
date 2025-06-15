from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .models import StatusEnum


class MessageResponse(BaseModel):
    message: str


class OrderList(BaseModel):
    id: int
    user_id: int
    total_amount: float
    created_at: datetime
    status: StatusEnum


class OrderItem(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: float

    model_config = ConfigDict(from_attributes=True)