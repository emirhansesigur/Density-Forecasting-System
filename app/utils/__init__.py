# from app.routes import predict, user

# app = None

# def create_app():
#     global app
#     from fastapi import FastAPI
#     app = FastAPI()
#     app.include_router(predict.router)
#     app.include_router(user.router)
#     return app

# create_app()


from fastapi import FastAPI
from app.routes import predict, user

app = FastAPI()

app.include_router(predict.router)
app.include_router(user.router)