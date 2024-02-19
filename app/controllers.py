from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["index"])
def index_route():
    return {"Hello": "Dashboard"}
