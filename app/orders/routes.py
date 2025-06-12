from app.auth.routes import get_db
from app.core.dependencies import require_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.cart.schemas import CartCreate
from . import controllers


router = APIRouter(prefix="", tags=["Checkout", "Orders"])


@router.post("/checkout")
def check_out(cartdetail: List[CartCreate], db: Session = Depends(get_db), current_user=Depends(require_user)):
    return controllers.checkout(cartdetail=cartdetail, db=db, current_user=current_user)


@router.get("/orders")
def get_orders(db: Session = Depends(get_db), current_user=Depends(require_user)):
    return controllers.show_orders(db=db, current_user=current_user)


@router.get("/orders/{order_id}")
def get_order_by_id(order_id: int, db: Session = Depends(get_db), current_user=Depends(require_user)):
    return controllers.fetch_order_by_id(db=db, current_user=current_user, order_id=order_id)