from app.core.database import Base
from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from sqlalchemy import Enum as SqlEnum
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from app.auth.models import User
from app.products.models import Products


class StatusEnum(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, index=True)
    total_amount = Column(Integer, nullable=False)
    status = Column(SqlEnum(StatusEnum), default=StatusEnum.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItems", back_populates="orders")


class OrderItems(Base):
    __tablename__ = "orderitems"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey(Orders.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Products.id), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Integer, nullable=False)

    orders = relationship("Orders", back_populates="items")
    products = relationship("Products", back_populates="items")