from fastapi import FastAPI
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



app.include_router(predict_router, prefix="/api")

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "API is running!"}