from fastapi import FastAPI

import models
from database import engine

def create_app(db_engine=engine):
    models.Base.metadata.create_all(bind=db_engine)
    app = FastAPI(title="Piazza API")

    @app.get("/health")
    def health():
        return {"status": "Ok"}

    return app