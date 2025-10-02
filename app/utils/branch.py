from enum import Enum

class BranchLocation(Enum):
    """
    Şube lokasyonlarını ve koordinatlarını içeren enum
    """
    ANTALYA = {
        "latitude": 36.9109,
        "longitude": 30.6772,
        "name": "Antalya"
    }
    
    # İleride başka şubeler eklenebilir
    # ISTANBUL = {
    #     "latitude": 41.0082,
    #     "longitude": 28.9784,
    #     "name": "Istanbul"
    # }
    
    # ANKARA = {
    #     "latitude": 39.9334,
    #     "longitude": 32.8597,
    #     "name": "Ankara"
    # }
    
    @classmethod
    def get_by_id(cls, branch_id: int):
        """
        Branch ID'ye göre enum değerini döndürür
        """
        branch_map = {
            1: cls.ANTALYA,
            # 2: cls.ISTANBUL,
            # 3: cls.ANKARA,
        }
        
        if branch_id not in branch_map:
            raise ValueError(f"Geçersiz branch ID: {branch_id}")
        
        return branch_map[branch_id]
    
    @classmethod
    def get_coordinates(cls, branch_id: int):
        """
        Branch ID'ye göre koordinatları döndürür
        """
        branch = cls.get_by_id(branch_id)
        return branch.value["latitude"], branch.value["longitude"]
    
    @classmethod
    def get_name(cls, branch_id: int):
        """
        Branch ID'ye göre şube ismini döndürür
        """
        branch = cls.get_by_id(branch_id)
        return branch.value["name"]