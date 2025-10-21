from enum import Enum

class BranchLocation(Enum):
    ANTALYA = {
        "latitude": 36.9109,
        "longitude": 30.6772,
        "name": "Antalya"
    }
    
    ISTANBUL = {
        "latitude": 41.0082,
        "longitude": 28.9784,
        "name": "Istanbul"
    }
    
    @classmethod
    def get_by_id(cls, branch_id: int):
        # Branch ID'ye göre enum değerini döndürür
        branch_map = {
            1: cls.ANTALYA,
            2: cls.ISTANBUL,
            # 3: cls.ANKARA,
        }
        
        if branch_id not in branch_map:
            raise ValueError(f"Geçersiz branch ID: {branch_id}")
        
        return branch_map[branch_id]
    
    @classmethod
    def get_coordinates(cls, branch_id: int):
        # Branch ID'ye göre koordinatları döndürür
        branch = cls.get_by_id(branch_id)
        return branch.value["latitude"], branch.value["longitude"]
    
    @classmethod
    def get_name(cls, branch_id: int):
        # Branch ID'ye göre şube ismini döndürür
        branch = cls.get_by_id(branch_id)
        return branch.value["name"]