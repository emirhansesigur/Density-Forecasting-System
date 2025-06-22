from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from app.utils.helpers import predict_users_logic
from app.utils.weather import get_weather_for_datetime_daily, get_weather_for_date_hourly

router = APIRouter()

LATITUDE = 36.9109
LONGITUDE = 30.6772


@router.post("/PredictUsersByHour") 
def PredictUsersByHour(input_data: dict):
    try:
        zaman_str = input_data.get("zaman")
        if not zaman_str:
            raise ValueError("zaman alanı zorunludur. (örn: '2025-07-01T17:00:00')")
        try:
            zaman = datetime.fromisoformat(zaman_str)
        except Exception:
            raise ValueError("zaman alanı ISO formatında olmalıdır. (örn: '2025-07-01T17:00:00')")
        saat = zaman.hour
        gün = zaman.day
        ay = zaman.month
        yıl = zaman.year

        haftanin_gunu = zaman.weekday()  # Pazartesi=0, Pazar=6
        hafta_sonu_mu = 1 if haftanin_gunu in [5, 6] else 0
        ozel_gun_mu = 0

        weather = get_weather_for_date_hourly(LATITUDE, LONGITUDE, zaman)
        
        # print("weather print edilitor")
        # print(weather)

        features = {
            "saat": saat,
            "gün": gün,
            "ay": ay,
            "yıl": yıl,
            "haftanin_gunu": haftanin_gunu,
            "hafta_sonu_mu": hafta_sonu_mu,
            "ozel_gun_mu": ozel_gun_mu,
            "temperature": weather["temperature"],
            "humidity": weather["humidity"],
            "precipitation": weather["precipitation"]
        }
        
        result = predict_users_logic(features)

        return {
            "tarih": zaman.strftime("%Y-%m-%d"),
            "saat": zaman.strftime("%H:%M"),
            "predicted_users": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/PredictUsersByDay")
def PredictUsersByDay(input_data: dict):
    """
    input_data: {
        "zaman": "2025-07-01",
        "ozel_gun_mu": 0
    }
    """
    try:
        zaman_str = input_data.get("zaman")
        if not zaman_str:
            raise ValueError("zaman alanı zorunludur. (örn: '2025-07-01')")
        try:
            zaman = datetime.fromisoformat(zaman_str)
        except Exception:
            raise ValueError("zaman alanı ISO formatında olmalıdır. (örn: '2025-07-01')")
        
        gün = zaman.day
        ay = zaman.month
        yıl = zaman.year

        haftanin_gunu = zaman.weekday()  # Pazartesi=0, Pazar=6
        hafta_sonu_mu = 1 if haftanin_gunu in [5, 6] else 0
        ozel_gun_mu = input_data.get("ozel_gun_mu", 0)

        results = []
        for saat in range(9, 22):  # 09:00'dan 21:00'a kadar
            dt = datetime(yıl, ay, gün, saat)
            weather = get_weather_for_datetime_daily(LATITUDE, LONGITUDE, dt)
            features = {
                "saat": saat,
                "gün": gün,
                "ay": ay,
                "yıl": yıl,
                "haftanin_gunu": haftanin_gunu,
                "hafta_sonu_mu": hafta_sonu_mu,
                "ozel_gun_mu": ozel_gun_mu,
                "temperature": weather["temperature"],
                "humidity": weather["humidity"],
                "precipitation": weather["precipitation"]
            }
            user_count = predict_users_logic(features)
            results.append({
                "tarih": dt.strftime("%Y-%m-%d"),
                "saat": dt.strftime("%H:%M"),
                "predictedUsers": user_count
            })

        return {"predictions": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
