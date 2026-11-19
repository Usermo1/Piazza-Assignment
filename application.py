from fastapi import FastAPI

import models
from database import engine
from routers import auth, posts

def create_app(db_engine=engine):
    models.Base.metadata.create_all(bind=db_engine)
    app = FastAPI(title="Piazza API")
    app.include_router(auth.router, prefix="/auth")
    app.include_router(posts.router, prefix="/posts")

    @app.get("/health")
    def health():
        return {"status": "Ok"}

    return app