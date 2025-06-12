from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from fastapi import Query
from . import controllers, schemas
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import dependencies
from app.core.logging_config import logger

router = APIRouter(prefix="/admin", tags=["Admin-Products"])


@router.post("/products", response_model=schemas.ProductOut)
async def add_product(product: schemas.ProductCreate, db: AsyncSession = Depends(get_db), current_user=Depends(dependencies.require_admin)):
    try:
        return await controllers.product_create(product=product, db=db, current_user=current_user)
    except Exception as e:
        logger.error(f"Something went wrong!: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add product! : {e}")


@router.get("/products")
async def get_all_products(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100),
                           db: AsyncSession = Depends(get_db), current_user=Depends(dependencies.require_admin)):
    try:
        result = await controllers.get_product_list(db=db, page=page, page_size=page_size, current_user=current_user)
        if not result:
            return {"message": "No products found!"}
        return result
    except Exception as e:
        logger.error(f"Something went wrong!: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch admin products! : {e}")


@router.get("/products/{id}")
async def get_product(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(dependencies.require_admin)):
    try:
        result = await controllers.get_product_by_id(db=db, id=id, current_user=current_user)
        if not result:
            return {"message": "No product found!"}
        return result
    except Exception as e:
        logger.error(f"Something went wrong!: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch product! : {e}")


@router.patch("/products/{id}")
async def update_product(id: int, product: schemas.ProductUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(dependencies.require_admin)):
    try:
        result = await controllers.update_product_details(id=id, product=product, db=db, current_user=current_user)
        if not result:
            raise HTTPException("Product not updated. Something went wrong....")
        return result
    except Exception as e:
        logger.error(f"Something went wrong!: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update product! : {e}")


@router.delete("/products/{id}")
async def delete_product(id: int, db: Session = Depends(get_db), current_user=Depends(dependencies.require_admin)):
    try:
        return await controllers.delete_product_by_id(id=id, db=db, current_user=current_user)
    except Exception as e:
        logger.error(f"Something went wrong!: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete product! : {e}")
