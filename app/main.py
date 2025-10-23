from fastapi import FastAPI
from app.routes.forecast import router as forecast_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend portları
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(forecast_router, prefix="/api")

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "API is running!"}