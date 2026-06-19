import os

from fastapi import UploadFile
from models import ResponseSignal
from .BaseController import BaseController
from .ProjectController import ProjectController
import regex as re


class DataController(BaseController):
    """Controller for handling file uploads and validation in the RAG system.

    Manages file validation (size and type checking), filename sanitization, and ensures
    unique filenames when storing uploaded documents for the RAG pipeline.
    """

    def __init__(self):
        super().__init__()  # configure the env data from .env file using pydantic settings inherited from Base Controller
        self.size_scale = 1048576  # convert MB to bytes
        project_controller = (
            ProjectController()
        )  # Initialize ProjectController to manage project directories

    def Validate_uploaded_file(self, file: UploadFile):
        """Validate an uploaded file against configured size and type restrictions.

        Args:
            file (UploadFile): FastAPI UploadFile object containing file metadata and content.

        Returns:
            tuple: (is_valid: bool, signal: str) - Validation result and corresponding ResponseSignal value.
        """
        # Check file size
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        # Check file type
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        return True, ResponseSignal.FILE_UPLOAD_SUCCESS.value

    def generate_unique_file_path(self, original_filename: str, project_id: str) -> str:
        """Generate a unique file path with a random prefix to prevent filename collisions.

        Args:
            original_filename (str): The original filename uploaded by the user.
            project_id (str): Unique identifier for the project directory.

        Returns:
            str: Full file path with sanitized filename prefixed by random string (format: 'random_key_filename') & file ID.
        """
        random_key = (
            self.generate_random_string()
        )  # Generate a random string of length 8
        project_path = ProjectController().Get_project_path(project_id=project_id)

        clean_filename = self.get_clean_filename(original_filename=original_filename)

        new_file_path = os.path.join(project_path, random_key + "_" + clean_filename)

        while os.path.exists(new_file_path):
            random_key = (
                self.generate_random_string()
            )  # Generate a new random string if the file already exists
            new_file_path = os.path.join(
                project_path, random_key + "_" + clean_filename
            )
        return new_file_path, random_key + "_" + clean_filename

    def get_clean_filename(self, original_filename: str) -> str:
        """Sanitize a filename by removing special characters and replacing spaces with underscores.

        Args:
            original_filename (str): The filename to clean, potentially containing special characters or spaces.

        Returns:
            str: Cleaned filename containing only word characters (letters, digits, underscore) and dots.
        """
        # Remove any unwanted characters from the filename
        clean_filename = re.sub(r"[^\w.]", "", original_filename.strip())
        clean_filename = clean_filename.replace(
            " ", "_"
        )  # Replace spaces with underscores
        return clean_filename
