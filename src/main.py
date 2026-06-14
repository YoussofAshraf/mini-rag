from fastapi import FastAPI
from routes import base, data

"""
Mini-RAG (Retrieval-Augmented Generation) API

Main entry point for the FastAPI application. Initializes the FastAPI app instance
and registers all route handlers for the RAG system including base health checks
and data upload functionality.
"""

app = FastAPI()

app.include_router(base.base_router)
app.include_router(data.data_router)
