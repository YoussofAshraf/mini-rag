from fastapi import APIRouter, Depends
from utils.config import Settings, get_settings

base_router = APIRouter(prefix="/api/v1", tags=["api_v1"])


@base_router.get("/welcome")
def welcome():
    """Welcome endpoint providing a greeting message to API users.

    Args:
        None

    Returns:
        dict: Welcome message for the mini RAG API.
    """
    return {"message": "Welcome to the mini RAG API!"}


@base_router.get("/")
async def health_check(app_settings: Settings = Depends(get_settings)):
    """Health check endpoint that returns application status and version information.

    Args:
        app_settings (Settings): Application settings injected via dependency injection.

    Returns:
        dict: Status information including app name and version.
    """
    # app_settings = get_settings()
    return {
        "status": "OK",
        "app_name": app_settings.APP_NAME,
        "version": app_settings.APP_VERSION,
    }
