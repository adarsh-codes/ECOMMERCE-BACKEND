from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from app.core.error_response import format_error
from app.core.database import Base, engine
from fastapi.openapi.utils import get_openapi
from app.auth import routes
from app.products import public_routes, admin_routes
from app.cart import routes as cart_routes
from app.orders import routes as order_routes
from app.middlewares.logging_middleware import LoggingMiddleware
from app.core.logging_config import logger
from app.core.dependencies import oauth2_scheme
from app.auth.models import User, PasswordToken
from app.cart.models import Cart
from app.orders.models import Orders, OrderItems
from app.products.models import Products


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="ECOMMERCE-BACKEND", version="1.0", lifespan=lifespan)


# Including all routers and middleware
app.include_router(routes.router)
app.add_middleware(LoggingMiddleware)
app.include_router(public_routes.router)
app.include_router(admin_routes.router)
app.include_router(cart_routes.router)
app.include_router(order_routes.router)


@app.get("/")
def main_app():
    return {"message": "Switch to localhost:8000/docs for Swagger UI."}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}")
    return format_error("Internal Server Error", 500)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Validation error occurred",
            "code": 422,
            "details": [
                {
                    "field": err["loc"][-1],
                    "message": err["msg"],
                    "type": err["type"]
                }
                for err in exc.errors()
            ]
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail if isinstance(exc.detail, str) else "Something went wrong",
            "code": exc.status_code,
            "detail": exc.detail if isinstance(exc.detail, dict) else None
        }
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="E-commerce API",
        version="1.0.0",
        description="Secure backend using JWT token auth",
        routes=app.routes,
    )
    # Override the OAuth2 security scheme to use Bearer
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for route in app.routes:
        if isinstance(route, APIRoute):
            if any(dep.dependencies == oauth2_scheme for dep in route.dependant.dependencies):
                path = route.path
                method = list(route.methods)[0].lower()
                openapi_schema["paths"][path][method]["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi