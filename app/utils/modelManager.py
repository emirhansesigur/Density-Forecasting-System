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
            1: {
                "games": "app/models/Antalya/antalya_games_rf_model.pkl",
                "players": "app/models/Antalya/antalya_unique_players_rf_model.pkl"
            },
            2: {
                "games": "app/models/Istanbul/istanbul_games_rf_model.pkl",
                "players": "app/models/Istanbul/istanbul_unique_players_rf_model.pkl"
            }
        }
        
        for branch_id, paths in model_paths.items():
            self._models[branch_id] = {}
            for model_type, model_path in paths.items():
                if os.path.exists(model_path):
                    try:
                        self._models[branch_id][model_type] = joblib.load(model_path)
                        branch_name = BranchLocation.get_name(branch_id)
                        print(f"{branch_name} {model_type} model loaded from {model_path}")
                    except Exception as e:
                        print(f"Error loading {model_path}: {str(e)}")
                else:
                    print(f"Model file not found: {model_path}")
    
    def get_model(self, branch_id: int, model_type: str = "games"):
        if branch_id not in self._models:
            available_branches = list(self._models.keys())
            raise ValueError(
                f"Model not found for branch ID {branch_id}. "
                f"Available branches: {available_branches}"
            )
        
        if model_type not in self._models[branch_id]:
            available_types = list(self._models[branch_id].keys())
            raise ValueError(
                f"Model type '{model_type}' not found for branch ID {branch_id}. "
                f"Available types: {available_types}"
            )
            
        return self._models[branch_id][model_type]
    
    def is_model_loaded(self, branch_id: int) -> bool:
        return branch_id in self._models
    
    def get_loaded_branches(self) -> list:
        return list(self._models.keys())

# Singleton instance
modelManager = ModelManager()