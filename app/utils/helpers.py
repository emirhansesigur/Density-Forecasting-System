import joblib
import pandas as pd
import os

model_path = "app/models/random_forest_model.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"{model_path} dosyası bulunamadı. Lütfen modeli yükleyin.")

model = joblib.load(model_path)

def predict_users_logic(input_data):
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    return int(prediction[0])
