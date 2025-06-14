from fastapi import APIRouter, Depends, HTTPException
from app.auth.routes import get_db, AsyncSession
from . import controllers, schemas
from app.core.dependencies import require_user
from app.core.logging_config import logger
from typing import List

router = APIRouter(prefix="/cart", tags=["Cart Items"])


@router.post("", response_model=schemas.CartCreate)
async def add_to_cart(cart: schemas.CartCreate, db: AsyncSession = Depends(get_db), current_user=Depends(require_user)):
    try:
        cart_items = await controllers.add_cart_item(db=db, user=current_user, cart=cart)
        if not cart_items:
            raise HTTPException(status_code=400, detail="Nothing added to cart!")
        return cart_items
    except Exception as e:
        logger.warning(f"Something went wrong : {e}")
        raise HTTPException(status_code=500, detail=f"Product not added to cart! : {e}")


@router.get("", response_model=List[schemas.CartItemResponse])
async def get_cart(db: AsyncSession = Depends(get_db), current_user=Depends(require_user)):
    try:
        items = await controllers.get_cart_items(db=db, user=current_user)
        if not items:
            raise HTTPException(status_code=400, detail="Cart is Empty!")
        return items
    except Exception as e:
        logger.warning(f"Something went wrong : {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch cart items! : {e}")


@router.delete("/{product_id}", response_model=schemas.MessageResponse)
async def delete_item(product_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_user)):
    try:
        result = await controllers.delete_cart_item(db=db, user=current_user, product_id=product_id)
        return result
    except Exception as e:
        logger.warning(f"Something went wrong : {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete cart item! : {e}")


@router.patch("/{product_id}", response_model=schemas.CartItemResponse)
async def update_quantity(cart: schemas.CartUpdate, product_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_user)):
    try:
        result = await controllers.update_cart(product_id=product_id, db=db, user=current_user, cart=cart)
        return result
    except Exception as e:
        logger.warning(f"Something went wrong : {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update cart item quantity! : {e}")
