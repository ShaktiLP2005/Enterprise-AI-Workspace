from fastapi import APIRouter, UploadFile, File

from app.services.document_service import save_document

router = APIRouter(
    prefix="/upload",
    tags=["Document Upload"]
)


@router.post("/")
def upload_document(file: UploadFile = File(...)):
    # Save the uploaded document
    saved_path = save_document(file)

    # Return a success response
    return {
        "message": "Document uploaded successfully.",
        "path": saved_path,
    }