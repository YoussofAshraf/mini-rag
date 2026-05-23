from fastapi import FastAPI,APIRouter
import os
base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)

@base_router.get("/welcome")
def welcome():
    return {"message": "Welcome to the mini RAG API!"}


@base_router.get("/")
async def health_check():
    return {
                "status": "OK",
                "app_name":os.getenv("APP_NAME","unknown"),
                "version":os.getenv("APP_VERSION","unknown")
            }
    