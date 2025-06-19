from fastapi import FastAPI
from app.routes import predict, user

app = FastAPI()

app.include_router(predict.router)
app.include_router(user.router)