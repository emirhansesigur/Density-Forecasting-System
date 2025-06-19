from fastapi import APIRouter

router = APIRouter(
    prefix="/api/users",
    tags=["usesr"]
)

@router.get("/")
async def user_root():
    return {"message": "User endpoint"}