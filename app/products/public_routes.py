from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from fastapi import Query
from typing import Optional, Literal
from . import controllers
from sqlalchemy.orm import Session

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def product_filters(
    category: Optional[str] = Query(None),
    min_price: Optional[int] = Query(None, ge=0),
    max_price: Optional[int] = Query(None, ge=0),
    sort_by: Optional[Literal["price_asc", "price_desc", "name_asc", "name_desc"]] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=0, le=100),
    db: Session = Depends(get_db)
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price cannot be greater than max_price")

    return controllers.get_products_filtered(
        db=db,
        category=category,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        page=page,
        page_size=page_size)


@router.get('/search')
def product_search(keyword: str = Query(None), db: Session = Depends(get_db)):
    return controllers.search_products(keyword=keyword)


@router.get('/{id}')
def get_product(db: Session = Depends(get_db)):
    return controllers.find_product(id=id, db=db)
