from fastapi import APIRouter

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
