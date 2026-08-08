from typing import Annotated

from fastapi import APIRouter, UploadFile, File

from app.services.document_processing_service import process_document


router = APIRouter(
    prefix="/upload",
    tags=["Document Upload"]
)


@router.post("/")
def upload_documents(
    files: Annotated[list[UploadFile], File(...)]
):
    """
    Upload and ingest multiple documents.
    """

    results = []

    for file in files:
        result = process_document(file)
        results.append(result)

    return {
        "message": "Documents uploaded and ingested successfully.",
        "documents": results
    }