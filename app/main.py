from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.predict import router as predict_router

app = FastAPI()

app.include_router(user_router, prefix="/api")
app.include_router(predict_router, prefix="/api")