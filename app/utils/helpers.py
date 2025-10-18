import joblib
import pandas as pd
import os

model_path = "app/models/OldAntalyaGamesForecastingRandomForest.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"{model_path} dosyası bulunamadı. Lütfen modeli yükleyin.")

model = joblib.load(model_path)

# todo: Branch Enum'a model seçilecek
# todo: Hız için modeller cache'lenebilir
def predictionLogic(input_data, branchId):
    print(f"Predicting with model for branch ID: {branchId}")
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    return int(prediction[0])
