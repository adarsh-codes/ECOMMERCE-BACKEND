from app.core.config import settings
from fastapi import FastAPI
from app.core.database import Base,engine
from app.auth import routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="My api",version="1.0")

app.include_router(routes.router)

@app.get('/')
def add_user():
    return {"hello":"yo"}
