from .models import Products
from sqlalchemy import asc, desc


def get_products_filtered(db, category, min_price, max_price, sort_by, page, page_size):
    query = db.query(Products)

    if category:
        query = query.filter(Products.category == category)
    if min_price:
        query = query.filter(Products.price >= min_price)
    if max_price:
        query = query.filter(Products.price <= max_price)

    if sort_by == "price_asc":
        query = query.order_by(asc(Products.price))
    elif sort_by == "price_desc":
        query = query.order_by(desc(Products.price))
    elif sort_by == "name_asc":
        query = query.order_by(asc(Products.name))
    elif sort_by == "name_desc":
        query = query.order_by(desc(Products.name))

    offset_value = (page - 1) * page_size
    product_list = query.offset(offset_value).limit(page_size).all()

    return product_list


def search_products(keyword, db):
    if not keyword:
        return db.query(Products).all()

    return db.query(Products).filter(Products.name.ilike(f"%{keyword}%")).all()


def find_product(id, db):
    query = db.query(Products).filter(Products.id == id).first()
    return query


def product_create(product, db):
    db_product = Products(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product_list(db, page, page_size):
    query = db.query(Products)
    offset_value = (page - 1) * page_size
    return query.offset(offset_value).limit(page_size).all()


def get_product_by_id(db, id):
    return db.query(Products).filter(Products.id == id).first()


def update_product_details(db, id, product):
    product_obj = db.query(Products).filter(Products.id == id).first()
    update_data = product.model_dump()
    for field, value in update_data.items():
        setattr(product_obj, field, value)
    db.add(product_obj)
    db.commit()
    db.refresh(product_obj)
    return update_data


def delete_product_by_id(id, db):
    db_product = db.query(Products).filter(Products.id == id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
