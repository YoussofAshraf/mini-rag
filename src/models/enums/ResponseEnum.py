from enum import Enum


class ResponseSignal(Enum):
    """Enumeration of signal responses for file upload operations.

    Provides standardized response codes for indicating file upload status,
    validation results, and error conditions.
    """

    FILE_TYPE_NOT_SUPPORTED = "FILE_TYPE_NOT_SUPPORTED"
    FILE_SIZE_EXCEEDED = "FILE_SIZE_EXCEEDED"
    FILE_UPLOAD_SUCCESS = "FILE_UPLOAD_SUCCESS"
    FILE_UPLOAD_FAILURE = "FILE_UPLOAD_FAILURE"
    FILE_PROCESSING_SUCCESS = "FILE_PROCESSING_SUCCESS"
    FILE_PROCESSING_FAILURE = "FILE_PROCESSING_FAILURE"
