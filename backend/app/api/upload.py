from fastapi import APIRouter, UploadFile, File

from app.services.document_processing_service import process_document


router = APIRouter(
    prefix="/upload",
    tags=["Document Upload"]
)


@router.post("/")
def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document.
    """

    return process_document(file)