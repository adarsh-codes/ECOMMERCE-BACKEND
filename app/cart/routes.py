from fastapi import APIRouter, Depends
from app.auth.routes import get_db, Session
from . import controllers, schemas
from app.core.dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/cart", tags=["Cart Items"])


@router.post("")
def add_to_cart(cart: schemas.CartCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return controllers.add_cart_item(db=db, user=current_user, cart=cart)


@router.get("")
def get_cart(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return controllers.get_cart_items(db=db, user=current_user)


@router.delete("/{product_id}")
def delete_item(product_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return controllers.delete_cart_item(db=db, user=current_user, product_id=product_id)


@router.patch("/{product_id}")
def update_quantity(cart: schemas.CartUpdate, product_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return controllers.update_cart(product_id=product_id, db=db, user=current_user, cart=cart)
