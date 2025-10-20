import joblib
import pandas as pd
import os

model_path = "app/models/Antalya/antalya_games_rf_model.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"{model_path} dosyası bulunamadı. Lütfen modeli yükleyin.")

model = joblib.load(model_path)

def get_hour_group(hour: int) -> str:
    if 9 <= hour <= 12:
        return 'early_hours'
    elif 13 <= hour <= 17:
        return 'afternoon'
    else:
        return 'evening_hours'

def get_season(month: int) -> str:
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'fall'



def forecastingLogic(inputData: dict):
    """
    {
        "branchId": 1,
        "hour": 10,
        "day": 5,
        "month": 10,
        "year": 2025,
        "dayOfWeek": 6,
        "isWeekend": 1,
        "temperature": 25.5,
        "humidity": 60,
        "precipitation": 50.0
    }
    """
    print(f"branchId: {inputData["branchId"]} - Predicting with model...")

    hour_group = get_hour_group(inputData["hour"])
    season = get_season(inputData["month"])


    model_features = {
        "hour": inputData["hour"],
        "day": inputData["day"],
        "month": inputData["month"],
        "year": inputData["year"],
        "dayofWeek": inputData["dayOfWeek"],
        "isWeekend": inputData["isWeekend"],
        "isSpecialDay": 1 if inputData["isSpecialDay"] else 0,
        "temperature": inputData["temperature"],
        "humidity": inputData["humidity"],
        "precipitation": inputData["precipitation"],
        "hour_group_afternoon": 1 if hour_group == "afternoon" else 0,
        "hour_group_early_hours": 1 if hour_group == "early_hours" else 0,
        "hour_group_evening_hours": 1 if hour_group == "evening_hours" else 0,
        "season_fall": 1 if season == "fall" else 0,
        "season_spring": 1 if season == "spring" else 0,
        "season_summer": 1 if season == "summer" else 0,
        "season_winter": 1 if season == "winter" else 0
    }

    df_features = pd.DataFrame([model_features])

    predicted_value = model.predict(df_features)[0]

    return int(predicted_value)


def predictionLogic(input_data, branchId):
    print(f"Predicting with model for branch ID: {branchId}")
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    return int(prediction[0])
