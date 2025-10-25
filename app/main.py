from fastapi import FastAPI
from app.routes.forecastGames import router as forecast_games_router
from app.routes.forecastUniquePlayers import router as forecast_unique_players_router
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

app.include_router(forecast_games_router, prefix="/api")
app.include_router(forecast_unique_players_router, prefix="/api")

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "API is running!"}