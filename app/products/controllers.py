from .models import Products
from sqlalchemy import asc, desc, select


async def get_products_filtered(db, category, min_price, max_price, sort_by, page, page_size):   
    statement = select(Products)

    if category:
        statement = statement.where(Products.category == category)
    if min_price:
        statement = statement.where(Products.price >= min_price)
    if max_price:
        statement = statement.where(Products.price <= max_price)

    if sort_by == "price_asc":
        statement = statement.order_by(asc(Products.price))
    elif sort_by == "price_desc":
        statement = statement.order_by(desc(Products.price))
    elif sort_by == "name_asc":
        statement = statement.order_by(asc(Products.name))
    elif sort_by == "name_desc":
        statement = statement.order_by(desc(Products.name))

    offset_value = (page - 1) * page_size
    statement = statement.offset(offset_value).limit(page_size)

    result = await db.execute(statement)
    product_list = result.scalars().all()

    return product_list


async def search_products(keyword, db):
    statement = select(Products)

    if not keyword:
        result = await db.execute(statement)
        product_list = result.scalars().all()
        return product_list

    result = await db.execute(select(Products).where(Products.name.ilike(f"%{keyword}%")))
    product_list = result.scalars().all()
    return product_list


async def find_product(id, db):
    statement = await db.execute(select(Products).where(Products.id == id))
    return statement.scalar_one_or_none()


async def product_create(product, db, current_user):
    db_product = Products(name=product.name, 
                          description=product.description,
                          price=product.price,
                          stock=product.stock,
                          image_url=product.image_url,
                          category=product.category,
                          user_id=current_user.id)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def get_product_list(db, page, page_size, current_user):
    query = select(Products).where(Products.user_id == current_user.id)
    offset_value = (page - 1) * page_size
    result = await db.execute(query.offset(offset_value).limit(page_size))
    return result.scalars().all()


async def get_product_by_id(db, id, current_user):
    query = select(Products).where(Products.id == id, Products.user_id == current_user.id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def update_product_details(db, id, product, current_user):
    query = select(Products).where(Products.id == id, Products.user_id == current_user.id)
    result = await db.execute(query)
    product_obj = result.scalar_one_or_none()
    update_data = product.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product_obj, field, value)
    db.add(product_obj)
    await db.commit()
    await db.refresh(product_obj)
    return update_data


async def delete_product_by_id(id, db, current_user):
    query = select(Products).where(Products.id == id, Products.user_id == current_user.id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()

    await db.delete(product)
    await db.commit()
    return {"message": "Deleted Product Successfully!"}
