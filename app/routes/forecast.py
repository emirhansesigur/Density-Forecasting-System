from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.utils.helpers import predictionLogic
from app.utils.weather import get_weather_for_datetime_daily, getWeatherForDateHourly
from app.utils.branch import BranchLocation

router = APIRouter()

# Pydantic model
class ForecastRequest(BaseModel):
    branchId: int
    date: str
    isSpecialDay: bool = False


@router.post("/forecast")
def forecast(request: ForecastRequest):
    try:
        branchId = request.branchId
        date_str = request.date
        isSpecialDay = 1 if request.isSpecialDay else 0
        
        print(f"Received forecast request: branchId={branchId}, date={date_str}, isSpecialDay={isSpecialDay}")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))