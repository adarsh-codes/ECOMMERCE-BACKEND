from pydantic import BaseModel, ConfigDict


class CartCreate(BaseModel):
    product_id: int
    quantity: int


class CartUpdate(BaseModel):
    quantity: int

    model_config = ConfigDict(from_attributes=True)