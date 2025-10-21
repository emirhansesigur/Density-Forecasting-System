# app/routers/forecast.py
from fastapi import APIRouter, HTTPException
from datetime import datetime
from pydantic import BaseModel
from app.utils.helpers import forecastingLogic
from app.utils.weather import getWeatherForDateHourly
from app.utils.branch import BranchLocation
from app.utils.model_manager import model_manager

router = APIRouter()

class ForecastRequest(BaseModel):
    date: str
    branchId: int
    isSpecialDay: bool

@router.post("/forecast")
def PredictGamesByDay(request: ForecastRequest):
    try:
        date_str = request.date
        branchId = request.branchId
        isSpecialDay = request.isSpecialDay

        if not date_str:
            raise ValueError("Date is required (e.g. '2025-10-02')")
        if branchId is None:
            raise ValueError("Branch ID is required.")
        if isSpecialDay is None:
            raise ValueError("Special day is required.")

        if not model_manager.is_model_loaded(branchId):
            available = model_manager.get_loaded_branches()
            raise ValueError(
                f"Branch ID {branchId} için model yüklü değil. "
                f"Mevcut branch'ler: {available}"
            )

        try:
            date = datetime.fromisoformat(date_str)
        except Exception:
            raise ValueError("Date must be in ISO format. (e.g. '2025-10-02')")

        try:
            latitude, longitude = BranchLocation.get_coordinates(branchId)
            branch_name = BranchLocation.get_name(branchId)
            print(f"Using branch {branchId} ({branch_name}) with coordinates: ({latitude}, {longitude})")
        except Exception:
            raise ValueError("Invalid Branch ID or branch enum not found.")
        
        day = date.day
        month = date.month
        year = date.year
        dayOfWeek = date.weekday()
        isWeekend = 1 if dayOfWeek in [5, 6] else 0
        
        hourlyPredictions = []
        
        for hour in range(10, 22):
            current_datetime = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            
            weather = getWeatherForDateHourly(latitude, longitude, current_datetime)
            
            inputData = {
                "hour": hour,
                "day": day,
                "month": month,
                "year": year,
                "dayOfWeek": dayOfWeek,
                "isWeekend": isWeekend,
                "temperature": weather["temperature"],
                "humidity": weather["humidity"],
                "precipitation": weather["precipitation"],
                "branchId": branchId,
                "isSpecialDay": isSpecialDay
            }
            
            predicted_games = forecastingLogic(inputData)
            
            hourlyPredictions.append({
                "hour": f"{hour:02d}:00",
                "predictedGames": round(predicted_games, 2),
                "temperature": weather["temperature"],
                "humidity": weather["humidity"],
                "precipitation": weather["precipitation"]
            })
        
        totalPredictedGames = sum(item["predictedGames"] for item in hourlyPredictions)
        
        return {
            "date": date.strftime("%Y-%m-%d"),
            "branchName": branch_name,
            "totalPredictedGames": round(totalPredictedGames, 2),
            "hourlyPredictions": hourlyPredictions
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))