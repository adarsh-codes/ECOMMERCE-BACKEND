from app.core.config import settings
from fastapi import FastAPI
from app.core.database import Base, engine
from app.auth import routes
from app.products import public_routes, admin_routes
from app.cart import routes as cart_routes
from app.middlewares.logging_middleware import LoggingMiddleware
from app.auth import models as auth_models
from app.cart import models as cart_models
from app.products import models as product_models


Base.metadata.create_all(bind=engine)

app = FastAPI(title="My api", version="1.0")

app.include_router(routes.router)
app.add_middleware(LoggingMiddleware)
app.include_router(public_routes.router)
app.include_router(admin_routes.router)
app.include_router(cart_routes.router)


@app.get('/')
def add_user():
    return {"hello": "yo"}
