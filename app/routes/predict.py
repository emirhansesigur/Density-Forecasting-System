from fastapi import APIRouter

router = APIRouter(
    prefix="/api/predict",
    tags=["predict"]
)

@router.get("/")
async def predict_root():
    return {"message": "Prediction endpoint"}