from .models import Products, OrderItems, Orders
from app.cart.models import Cart
from app.auth.models import User


def checkout(db, current_user, cartdetail):
    total_price = 0
    order_items = []

    for item in cartdetail:
        prod_id = item.product_id
        price = db.query(Products).filter(Products.id == prod_id).first().price
        prod_quantity = item.quantity
        price_at_purchase = price * prod_quantity
        total_price += price * prod_quantity

        order_items.append({"product_id": prod_id, "quantity": prod_quantity,
                            "price_at_purchase": price_at_purchase})

    user_id = db.query(User).filter(User.id == Cart.user_id).first().id
    order_obj = Orders(user_id=user_id, total_amount=total_price)
    db.add(order_obj)
    db.commit()
    db.refresh(order_obj)

    for item in order_items:
        order_item = OrderItems(
            order_id=order_obj.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price_at_purchase=item["price_at_purchase"]
        )
        db.add(order_item)

    db.commit()

    db.query(Cart).filter(Cart.user_id == current_user.id).delete()
    db.commit()

    return {"message": f"Order Placed order_id : {order_obj.id}, Amount debited :{total_price}! Thanks for shopping!"}


def show_orders(db, current_user):
    return db.query(Orders).filter(Orders.user_id == current_user.id).all()


def fetch_order_by_id(db, current_user, order_id):
    return db.query(Orders).filter(Orders.id == order_id).all()
