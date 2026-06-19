
import os

from controllers import BaseController, ProjectController
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessEnum

class ProcessController(BaseController):
    """
    Controller class for handling data processing operations.

    Inherits from BaseController to utilize shared configurations and methods.
    """
    def __init__(self,project_id:str):
        project_controller = ProjectController()  # Initialize ProjectController to manage project-related operations
        self.project_id = project_id  # Store the project ID for processing 
        self.project_path = project_controller.Get_project_path(project_id=self.project_id)  # Get the project path using ProjectController
        super().__init__()  # Initialize BaseController to configure environment data from .env file using pydantic settings

    def get_file_extenstion(self,file_id:str)->str:
        """
        Extracts the file extension from a given filename.

        Args:
            file_id (str): The ID of the file from which to extract the extension.

        Returns:
            str: The file extension, including the leading dot (e.g., '.txt').
        """
        return os.path.splitext(file_id)[-1]  # Use os.path.splitext to get the file extension
    
    def get_file_loader(self,file_id:str):
        """
        Determines the appropriate file loader based on the file extension.

        Args:
            file_id (str): The ID of the file for which to determine the loader.

        Returns:
            A document loader instance suitable for the file type.
        """
        file_extension = self.get_file_extenstion(file_id=file_id)
        file_path=os.path.join(self.project_path, file_id)  # Construct the full file path using the project path and file ID

        if file_extension in [ProcessEnum.PDF.value]:
            return PyMuPDFLoader(file_path)  # PyMuPDFLoader does not accept an encoding argument
        
        if file_extension in [ProcessEnum.TXT.value]:
            return TextLoader(file_path,encoding="utf-8")  # Use TextLoader for text files
        
        return None 

    def get_file_content(self, file_id:str):
        loader = self.get_file_loader(file_id=file_id) 
        return loader.load() if loader else None  # Load the file content using the appropriate loader, or return None if no loader is found 

    def process_file_content(self, file_content:list, file_id:str,chunk_size:int=100,chunk_overlap:int=20):
        """
        Processes the content of a file by splitting it into smaller chunks.

        Args:
            file_content (list): The content of the file to be processed.
            file_id (str): The ID of the file being processed.
            chunk_size (int): The maximum size of each chunk.
            chunk_overlap (int): The overlap between chunks.
        Returns:
            list: A list of text chunks obtained from splitting the file content.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,  # Define the maximum size of each chunk
            chunk_overlap=chunk_overlap,  # Define the overlap between chunks
            length_function=len  # Use the built-in len function to measure chunk length
        )
        # GEt file content texts List 
        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]
        
        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]
        
        
        chunks= text_splitter.create_documents(file_content_texts, metadatas=file_content_metadata)  # Split the documents into chunks and return them
        return chunks
