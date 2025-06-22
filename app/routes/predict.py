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

# @router.post("/PredictUsersByDay")
# def PredictUsersByDay(input_data: dict):
#     """
#     input_data: {
#         "zaman": "2025-07-01",
#         "ozel_gun_mu": 0
#     }
#     """
#     try:
#         zaman_str = input_data.get("zaman")
#         if not zaman_str:
#             raise ValueError("zaman alanı zorunludur. (örn: '2025-07-01')")
        
#         try:
#             zaman = datetime.fromisoformat(zaman_str)
#         except Exception:
#             raise ValueError("zaman alanı ISO formatında olmalıdır. (örn: '2025-07-01')")

#         gün = zaman.day
#         ay = zaman.month
#         yıl = zaman.year

#         haftanin_gunu = zaman.weekday()  # Pazartesi=0, Pazar=6
#         hafta_sonu_mu = 1 if haftanin_gunu in [5, 6] else 0
#         ozel_gun_mu = input_data.get("ozel_gun_mu", 0)

#         # 🌦 Sadece 1 defa veri çek
#         full_weather = get_weather_for_datetime_daily(LATITUDE, LONGITUDE, zaman)

#         # Saat bazlı verileri oku
#         weather_times = full_weather["hourly"]["time"]
#         temperatures = full_weather["hourly"]["temperature_2m"]
#         humidities = full_weather["hourly"]["relative_humidity_2m"]
#         precipitations = full_weather["hourly"]["precipitation"]

#         results = []

#         for saat in range(9, 22):  # 09:00 - 21:00 arası
#             # Hedef saat string formatında: "YYYY-MM-DDTHH:MM"
#             target_time_str = zaman.replace(hour=saat).strftime("%Y-%m-%dT%H:00")

#             if target_time_str in weather_times:
#                 idx = weather_times.index(target_time_str)

#                 features = {
#                     "saat": saat,
#                     "gün": gün,
#                     "ay": ay,
#                     "yıl": yıl,
#                     "haftanin_gunu": haftanin_gunu,
#                     "hafta_sonu_mu": hafta_sonu_mu,
#                     "ozel_gun_mu": ozel_gun_mu,
#                     "temperature": temperatures[idx],
#                     "humidity": humidities[idx],
#                     "precipitation": precipitations[idx]
#                 }

#                 user_count = predict_users_logic(features)

#                 results.append({
#                     "tarih": zaman.strftime("%Y-%m-%d"),
#                     "saat": f"{saat:02d}:00",
#                     "predictedUsers": user_count
#                 })
#             else:
#                 raise ValueError(f"{target_time_str} saatlik verisi bulunamadı.")

#         return {"predictions": results}

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))



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

        # 🌦 1 kez veri çek
        full_weather = get_weather_for_datetime_daily(LATITUDE, LONGITUDE, zaman)
        hourly_data = full_weather["hourly"]

        weather_times = hourly_data["time"]
        temperatures = hourly_data["temperature_2m"]
        humidities = hourly_data["relative_humidity_2m"]
        precipitations = hourly_data["precipitation"]

        results = []

        for saat in range(9, 22):  # 09:00 - 21:00 arası
            target_time_str = zaman.replace(hour=saat).strftime("%Y-%m-%dT%H:00")
            
            if target_time_str in weather_times:
                idx = weather_times.index(target_time_str)

                features = {
                    "saat": saat,
                    "gün": gün,
                    "ay": ay,
                    "yıl": yıl,
                    "haftanin_gunu": haftanin_gunu,
                    "hafta_sonu_mu": hafta_sonu_mu,
                    "ozel_gun_mu": ozel_gun_mu,
                    "temperature": temperatures[idx],
                    "humidity": humidities[idx],
                    "precipitation": precipitations[idx]
                }

                user_count = predict_users_logic(features)

                print(temperatures[idx], humidities[idx], precipitations[idx])
                print(f"Predicted users for {zaman.strftime('%Y-%m-%d')} at {saat}:00 -> {user_count}")

                results.append({
                    "tarih": zaman.strftime("%Y-%m-%d"),
                    "saat": f"{saat:02d}:00",
                    "predictedUsers": user_count
                })
            else:
                raise ValueError(f"{target_time_str} saatlik verisi bulunamadı.")

        return {"predictions": results}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
