from pydantic import BaseModel, ConfigDict


class CartCreate(BaseModel):
    product_id: int
    quantity: int


class CartUpdate(BaseModel):
    quantity: int


class MessageResponse(BaseModel):
    message: str


class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)