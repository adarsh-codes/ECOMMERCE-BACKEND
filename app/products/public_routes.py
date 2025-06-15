from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from fastapi import Query
from typing import Optional, Literal
from . import controllers
from . import schemas
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging_config import logger

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[schemas.ProductFetch])
async def product_filters(
    category: Optional[str] = Query(None),
    min_price: Optional[int] = Query(None, ge=0),
    max_price: Optional[int] = Query(None, ge=0),
    sort_by: Optional[Literal["price_asc", "price_desc", "name_asc", "name_desc"]] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price cannot be greater than max_price")

    try:
        result = await controllers.get_products_filtered(db=db, category=category, min_price=min_price,
                                                         max_price=max_price,
                                                         sort_by=sort_by,
                                                         page=page,
                                                         page_size=page_size)
        if not result:
            return {"message": "No products found!"}
        return result
    except Exception as e:
        logger.error(f"Something went wrong!: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch products : {e}")


@router.get('/search', response_model=List[schemas.ProductFetch])
async def product_search(keyword: str = Query(None), db: AsyncSession = Depends(get_db)):
    try:
        return await controllers.search_products(keyword=keyword, db=db)
    except Exception as e:
        logger.error(f"Something went wrong!: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch products : {e}")


@router.get('/{id}', response_model=schemas.ProductFetch)
async def get_product(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await controllers.find_product(id=id, db=db)
    except Exception as e:
        logger.error(f"Something went wrong!: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch products : {e}")
