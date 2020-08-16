from fastapi import APIRouter

base = APIRouter()


@base.get("/")
async def root():
    return {"result": "success", "message": "Api is up!"}
