from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.utils.helpers import predict_users_logic
from app.utils.weather import get_weather_for_datetime_daily, get_weather_for_date_hourly
from app.utils.branch import BranchLocation

router = APIRouter()

# Pydantic model'ler
class PredictByHourRequest(BaseModel):
    branch: int
    date: str
    isSpecialDay: bool = False

class PredictByDayRequest(BaseModel):
    branch: int
    date: str
    isSpecialDay: bool = False

@router.post("/PredictUsersByHour") 
def PredictUsersByHour(request: PredictByHourRequest):
    try:
        branch = request.branch
        date_str = request.date
        isSpecialDay = 1 if request.isSpecialDay else 0

        if not date_str:
            raise ValueError("date alanı zorunludur. (örn: '2025-07-01T17:00:00')")
        try:
            date = datetime.fromisoformat(date_str)
        except Exception:
            raise ValueError("date alanı ISO formatında olmalıdır. (örn: '2025-07-01T17:00:00')")


        try:
            # Düzeltilmiş enum kullanımı
            latitude, longitude = BranchLocation.get_coordinates(branch)
            branch_name = BranchLocation.get_name(branch)
            print(f"Using branch {branch} ({branch_name}) with coordinates: ({latitude}, {longitude})")
        except Exception:
            raise ValueError("Geçersiz branch ID veya branch enum'u bulunamadı.")


        hour = date.hour
        day = date.day
        month = date.month
        year = date.year

        dayOfWeek = date.weekday()  # Pazartesi=0, Pazar=6
        isWeekendEnd = 1 if dayOfWeek in [5, 6] else 0
        
        weather = get_weather_for_date_hourly(latitude, longitude, date)
        
        features = {
            "saat": hour,
            "gün": day,
            "ay": month,
            "yıl": year,
            "haftanin_gunu": dayOfWeek,
            "hafta_sonu_mu": isWeekendEnd,
            "ozel_gun_mu": isSpecialDay,
            "temperature": weather["temperature"],
            "humidity": weather["humidity"],
            "precipitation": weather["precipitation"]
        }
        
        result = predict_users_logic(features)

        return {
            "date": date.strftime("%Y-%m-%d"),
            "hour": date.strftime("%H:%M"),
            "branch": branch_name,
            "isSpecialDay": bool(isSpecialDay),
            "predicted_users": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/PredictUsersByDay")
def PredictUsersByDay(request: PredictByDayRequest):
    try:
        branch = request.branch
        date_str = request.date
        isSpecialDay = 1 if request.isSpecialDay else 0
        
        if not date_str:
            raise ValueError("date alanı zorunludur. (örn: '2025-10-02')")
        
        try:
            # Sadece tarih kısmını parse et
            date = datetime.fromisoformat(date_str)
        except Exception:
            raise ValueError("date alanı ISO formatında olmalıdır. (örn: '2025-10-02')")
        
        try:
            latitude, longitude = BranchLocation.get_coordinates(branch)
            branch_name = BranchLocation.get_name(branch)
            print(f"Using branch {branch} ({branch_name}) with coordinates: ({latitude}, {longitude})")
        except Exception:
            raise ValueError("Geçersiz branch ID veya branch enum'u bulunamadı.")
        
        # Temel tarih bilgileri
        day = date.day
        month = date.month
        year = date.year
        dayOfWeek = date.weekday()  # Pazartesi=0, Pazar=6
        isWeekendEnd = 1 if dayOfWeek in [5, 6] else 0
        
        # 10:00 - 21:00 arası tahminler
        hourly_predictions = []
        
        for hour in range(10, 22):  # 10'dan 21'e kadar (21 dahil)
            # O saate ait datetime oluştur
            current_datetime = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            
            # Hava durumu bilgisini al
            weather = get_weather_for_date_hourly(latitude, longitude, current_datetime)
            
            # Tahmin için features hazırla
            features = {
                "saat": hour,
                "gün": day,
                "ay": month,
                "yıl": year,
                "haftanin_gunu": dayOfWeek,
                "hafta_sonu_mu": isWeekendEnd,
                "ozel_gun_mu": isSpecialDay,
                "temperature": weather["temperature"],
                "humidity": weather["humidity"],
                "precipitation": weather["precipitation"]
            }
            
            # Tahmin yap
            predicted_users = predict_users_logic(features)
            
            # Sonucu listeye ekle
            hourly_predictions.append({
                "hour": f"{hour:02d}:00",
                "predicted_users": predicted_users,
                "temperature": weather["temperature"],
                "humidity": weather["humidity"],
                "precipitation": weather["precipitation"]
            })
        
        return {
            "date": date.strftime("%Y-%m-%d"),
            "branch": branch_name,
            "isSpecialDay": bool(isSpecialDay),
            "hourly_predictions": hourly_predictions,
            "total_predicted_users": sum(pred["predicted_users"] for pred in hourly_predictions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))