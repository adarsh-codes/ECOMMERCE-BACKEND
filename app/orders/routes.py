from app.auth.routes import get_db
from app.core.dependencies import require_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.cart.schemas import CartCreate
from . import controllers
from app.core.logging_config import logger


router = APIRouter(prefix="", tags=["Checkout", "Orders"])


@router.post("/checkout")
async def check_out(cartdetail: List[CartCreate], db: AsyncSession = Depends(get_db), current_user=Depends(require_user)):
    try:
        return await controllers.checkout(cartdetail=cartdetail, db=db, current_user=current_user)
    except Exception as e:
        logger.warning(f"Something went wrong... : {e}")
        raise HTTPException(status_code=500, detail=f"Checkout failed! : {e}")


@router.get("/orders")
async def get_orders(db: AsyncSession = Depends(get_db), current_user=Depends(require_user)):
    try:
        return await controllers.show_orders(db=db, current_user=current_user)
    except Exception as e:
        logger.warning(f"Something went wrong... : {e}")
        raise HTTPException(status_code=500, detail=f"Orders fetch failed! : {e}")


@router.get("/orders/{order_id}")
async def get_order_by_id(order_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_user)):
    try:
        return controllers.fetch_order_by_id(db=db, current_user=current_user, order_id=order_id)
    except Exception as e:
        logger.warning(f"Something went wrong... : {e}")
        raise HTTPException(status_code=500, detail=f"Order: {order_id} fetch failed! : {e}")
