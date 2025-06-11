from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.auth.models import User
from app.products.models import Products


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    product_id = Column(Integer, ForeignKey(Products.id), index=True, nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship("Products", back_populates="cart")
    user = relationship("User", back_populates="cart")