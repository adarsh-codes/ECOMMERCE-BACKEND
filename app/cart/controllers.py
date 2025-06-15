from .models import Cart
from app.products.models import Products
from app.auth.models import User
from sqlalchemy import select
from fastapi import HTTPException


async def add_cart_item(db, cart, user):
    query = select(Products).where(Products.id == cart.product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < cart.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    # Check if item already exists in cart
    result = await db.execute(
        select(Cart).where(Cart.product_id == cart.product_id, Cart.user_id == user.id)
    )
    existing_cart_item = result.scalar_one_or_none()

    if existing_cart_item:
        # Update quantity
        new_quantity = existing_cart_item.quantity + cart.quantity

        if product.stock < cart.quantity:
            raise HTTPException(status_code=400, detail="Not enough stock to increase quantity")

        existing_cart_item.quantity = new_quantity
        await db.commit()
        await db.refresh(existing_cart_item)
    else:
        # Create new cart item
        cart_obj = Cart(product_id=cart.product_id, user_id=user.id, quantity=cart.quantity)
        db.add(cart_obj)
        await db.commit()
        await db.refresh(cart_obj)
        existing_cart_item = cart_obj

    return existing_cart_item


async def get_cart_items(db, user):
    query = select(Cart).where(Cart.user_id == user.id)
    result = await db.execute(query)
    return result.scalars().all()


async def delete_cart_item(db, user, product_id):
    query = select(Cart).where(Cart.user_id == user.id, Cart.product_id == product_id)
    res_mid = await db.execute(query)
    result = res_mid.scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail="Product not found!")
    await db.delete(result)
    await db.commit()
    return {"message": f"Product_id : {product_id} item deleted from the cart."}


async def update_cart(db, user, product_id, cart):
    result = await db.execute(select(Products).where(Products.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    if cart.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1.")

    if cart.quantity > product.stock:
        raise HTTPException(status_code=400, detail=f"Only {product.stock} items available in stock.")

    query = select(Cart).where(Cart.user_id == user.id, Cart.product_id == product_id)
    result = await db.execute(query)
    cart_item = result.scalar_one_or_none()
    update_data = cart.model_dump()
    for field, value in update_data.items():
        setattr(cart_item, field, value)
    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)
    return update_data
