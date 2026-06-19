import os

from controllers import BaseController


class ProjectController(BaseController):
    """Controller for managing project directories and file organization.

    Handles creation and retrieval of project-specific directories where uploaded
    files are stored and organized by project ID.
    """

    def __init__(self):
        super().__init__()

    def Get_project_path(self, project_id: str) -> str:
        """Get or create the directory path for a specific project.

        Args:
            project_id (str): Unique identifier for the project.

        Returns:
            str: Full file system path to the project's directory. Creates directory if it doesn't exist.
        """
        project_path = os.path.join(self.files_dir, project_id)

        if not os.path.exists(project_path):
            os.makedirs(project_path)

        return project_path
