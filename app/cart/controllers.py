from .models import Cart
from app.auth.models import User


def add_cart_item(db, cart, user):
    user_id = db.query(User).filter(User.id == user.id).first().id
    cart_obj = Cart(product_id=cart.product_id, user_id=user_id, quantity=cart.quantity)
    db.add(cart_obj)
    db.commit()
    db.refresh(cart_obj)
    return cart_obj


def get_cart_items(db, user):
    return db.query(Cart).filter(Cart.user_id == user.id).all()


def delete_cart_item(db, user, product_id):
    query = db.query(Cart).filter(Cart.product_id == product_id, Cart.user_id == user.id).first()
    db.delete(query)
    db.commit()
    return {"message": f"{query} item(s) deleted from the cart."}


def update_cart(db, user, product_id, cart):
    cart_item = db.query(Cart).filter(Cart.user_id == user.id, Cart.product_id == product_id).first()
    update_data = cart.model_dump()
    for field, value in update_data.items():
        setattr(cart_item, field, value)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return update_data