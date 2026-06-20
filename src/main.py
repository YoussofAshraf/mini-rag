from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import get_settings
"""
Mini-RAG (Retrieval-Augmented Generation) API

Main entry point for the FastAPI application. Initializes the FastAPI app instance
and registers all route handlers for the RAG system including base health checks
and data upload functionality.
"""

app = FastAPI()

@app.on_event("startup")
async def mongo_startup():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]


@app.on_event("shutdown")
async def mongo_shutdown():
    app.mongo_conn.close()

    
app.include_router(base.base_router)
app.include_router(data.data_router)