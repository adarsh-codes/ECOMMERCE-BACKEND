from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    stock: int
    category: str
    image_url: str


class ProductOut(ProductCreate):
    id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    image_url: Optional[str] = None


class ProductFetch(BaseModel):
    id: int
    user_id: int
    name: str
    description: str
    price: float
    stock: int
    category: str
    image_url: str


class MessageResponse(BaseModel):
    message: str

    model_config = ConfigDict(from_attributes=True)
