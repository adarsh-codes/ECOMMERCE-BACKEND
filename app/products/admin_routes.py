from fastapi import APIRouter, Depends
from app.core.database import get_db
from fastapi import Query
from . import controllers, schemas
from sqlalchemy.orm import Session
from app.core import dependencies

router = APIRouter(prefix="/admin", tags=["Admin-Products"])


@router.post("/products", response_model=schemas.ProductOut)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user=Depends(dependencies.require_admin)):
    return controllers.product_create(product=product, db=db)


@router.get("/products")
def get_all_products(page: int = Query(1, ge=1), page_size: int = Query(10, ge=0, le=100),
                     db: Session = Depends(get_db), current_user=Depends(dependencies.require_admin)):
    return controllers.get_product_list(db=db, page=page, page_size=page_size)


@router.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db), current_user=Depends(dependencies.require_admin)):
    return controllers.get_product_by_id(db=db, id=id)


@router.patch("/products/{id}")
def update_product(id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db), current_user=Depends(dependencies.require_admin)):
    return controllers.update_product_details(id=id, product=product, db=db)


@router.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db), current_user=Depends(dependencies.require_admin)):
    controllers.delete_product_by_id(id=id, db=db)
    return {"message": "Deleted Product Successfully!"}
