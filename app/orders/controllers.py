from .models import Products, OrderItems, Orders
from app.cart.models import Cart
from sqlalchemy import select
from fastapi import HTTPException


async def checkout(db, current_user, cartdetail):
    total_price = 0
    order_items = []

    for item in cartdetail:
        prod_id = item.product_id
        result = await db.execute(select(Products).where(Products.id == prod_id))
        prod = result.scalar_one_or_none()

        if not prod:
            raise HTTPException(status_code=404, detail=f"Product with id {prod_id} not found")
        if prod.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {prod.name}")

        # Deduct stock
        prod.stock -= item.quantity
        await db.flush()

        price = prod.price
        total_price += price * item.quantity

        order_items.append({
            "product_id": prod_id,
            "quantity": item.quantity,
            "price_at_purchase": price
        })

    # Create order
    order_obj = Orders(user_id=current_user.id, total_amount=total_price)
    db.add(order_obj)
    await db.flush()

    # Create order items
    for item in order_items:
        db.add(OrderItems(
            order_id=order_obj.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price_at_purchase=item["price_at_purchase"]
        ))
        await db.flush()

    # Clear user's cart
    cart_query = select(Cart).where(Cart.user_id == current_user.id)
    cart_result = await db.execute(cart_query)
    cart_items = cart_result.scalars().all()
    for cart_item in cart_items:
        await db.delete(cart_item)

    await db.commit()
    await db.refresh(order_obj)

    return {
        "message": f"Order Placed: order_id={order_obj.id}, Amount debited: Rs.{total_price}. Thank you for shopping!"
    }


async def show_orders(db, current_user):
    result = await db.execute(select(Orders).where(Orders.user_id == current_user.id).order_by(Orders.created_at.desc()))
    orders = result.scalars().all()
    return orders


async def fetch_order_by_id(db, current_user, order_id):
    result = await db.execute(select(Orders).where(Orders.user_id == current_user.id, Orders.id == order_id))
    order = result.scalar_one_or_none()
    return order
