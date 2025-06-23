from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.predict import router as predict_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware ekleyin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend portları
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(user_router, prefix="/api")
app.include_router(predict_router, prefix="/api")