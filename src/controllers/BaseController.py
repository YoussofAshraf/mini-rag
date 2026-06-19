import string

from utils.config import Settings, get_settings
import random
import os


class BaseController:
    """Base controller class providing shared functionality and configuration for all controllers.

    Manages application settings, file directory paths, and utility methods used across
    the RAG system for file handling and project management.
    """

    def __init__(self, app_settings: Settings = None):
        """Initialize the BaseController with application settings and file directories.

        Args:
            app_settings (Settings): Optional Pydantic Settings object. If not provided, loads from environment variables.

        Returns:
            None
        """

        self.app_settings = app_settings or get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.base_dir, "assets", "files")

    def generate_random_string(self, length: int = 12) -> str:
        """Generate a random alphanumeric string for unique file naming.

        Args:
            length (int): The desired length of the random string. Defaults to 12 characters.

        Returns:
            str: A random string containing letters (uppercase and lowercase) and digits.
        """
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))
