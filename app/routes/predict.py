from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/predictByDay")
def predictUsersByDay(input_data: dict):
    # Örnek kullanıcı verisi
    users = [
        {"id": 1, "name": "Ali"},
        {"id": 2, "name": "Ayşe"},
        {"id": 3, "name": "Mehmet"}
    ]
    return {"users": users}

@router.post("/denemeGetDailyPredictedUsers") 
def denemeGetDailyPredictedUsers(input_data: dict):
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

        #weather = get_weather_for_datetime(LATITUDE, LONGITUDE, zaman)

        features = {
            "saat": saat,
            "gün": gün,
            "ay": ay,
            "yıl": yıl,
            "haftanin_gunu": haftanin_gunu,
            "hafta_sonu_mu": hafta_sonu_mu,
            "ozel_gun_mu": ozel_gun_mu,
            "temperature":1,
            "humidity": 1,
            "precipitation": 1
        }
        #result = predict_users_logic(features)
        return {
            "tarih": zaman.strftime("%Y-%m-%d"),
            "saat": zaman.strftime("%H:%M"),
            #"predicted_users": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

