import joblib
import os
from typing import Dict
from app.utils.branch import BranchLocation

#Todo: uzun süre istek atılmazsa modeli bellekten atıp istek atılınca tekrar yükleme
class ModelManager:
    # Singleton class that manages all branch models

    _instance = None
    _models: Dict[int, any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance._load_models()
        return cls._instance
    
    def _load_models(self):
        model_paths = {
            1: "app/models/Antalya/antalya_games_rf_model.pkl",
            2: "app/models/Istanbul/istanbul_games_rf_model.pkl"
        }
        
        for branch_id, model_path in model_paths.items():
            if os.path.exists(model_path):
                try:
                    self._models[branch_id] = joblib.load(model_path)
                    branch_name = BranchLocation.get_name(branch_id)
                    print(f"{branch_name} model loaded from {model_path}")
                except Exception as e:
                    print(f"Error loading {model_path}: {str(e)}")
            else:
                print(f"Model file not found: {model_path}")
    
    def get_model(self, branch_id: int):

        if branch_id not in self._models:
            available_branches = list(self._models.keys())
            raise ValueError(
                f"Model not found for branch ID {branch_id}. "
                f"Available branches: {available_branches}"
            )
        return self._models[branch_id]
    
    def is_model_loaded(self, branch_id: int) -> bool:
        return branch_id in self._models
    
    def get_loaded_branches(self) -> list:
        return list(self._models.keys())

# Singleton instance
modelManager = ModelManager()