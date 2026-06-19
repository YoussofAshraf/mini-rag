import os

from fastapi import UploadFile, APIRouter, Depends, File, status
from fastapi.responses import JSONResponse

from controllers import DataController, ProjectController,ProcessController

from models.enums.ResponseEnum import ResponseSignal
from utils.config import Settings, get_settings
import aiofiles
import logging

from .schemas.data import ProcessRequest
# logger configuration to dagnosis any exceptions from log files
logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])

data_controller = DataController()
project_controller = ProjectController()


@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile = File(...),
    app_settings: Settings = Depends(get_settings),
):
    """Handle file uploads for a specific project with validation and storage.

    Args:
        project_id (str): Unique identifier for the target project.
        file (UploadFile): The uploaded file with content and metadata.
        app_settings (Settings): Application settings injected via dependency injection.

    Returns:
        JSONResponse: Upload status with signal (success/failure) and file ID.
    """

    is_valid, result_signal = data_controller.Validate_uploaded_file(file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal},
        )

    project_dir_path = project_controller.Get_project_path(project_id)
    file_path,file_id = data_controller.generate_unique_file_path(
        original_filename=file.filename,
        project_id=project_id
    )

    try: 
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error occurred while saving file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value},
        )
        
        
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"signal":  ResponseSignal.FILE_UPLOAD_SUCCESS.value, "file_id": file_id},
    )


@data_router.post("/process/{project_id}")
async def process_data(
    project_id:str,
    process_request: ProcessRequest,
):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset
    
    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        chunk_overlap=overlap_size
    )
    result = [
        {
            "page_content": chunk.page_content,
            "metadata": chunk.metadata
        }
        for chunk in file_chunks
    ]
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"signal": ResponseSignal.FILE_PROCESSING_SUCCESS.value, "chunks": result},
    ) if file_chunks else JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"signal": ResponseSignal.FILE_PROCESSING_FAILED.value},
    )
    
