from fastapi import FastAPI
from app.db import models
from app.db.database import engine
from app.api.routes import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)


@app.get("/")
def root():
    return {"message": "PayBridge is running"}
