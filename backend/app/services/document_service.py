from pathlib import Path
import shutil
import uuid

from fastapi import UploadFile

from app.core.config import settings


UPLOAD_DIR = Path(settings.UPLOAD_DIR)

# Create the upload directory if it doesn't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_document(file: UploadFile):
    """
    Save an uploaded document and generate a unique document ID.
    """

    document_id = str(uuid.uuid4())

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "document_id": document_id,
        "filename": file.filename,
        "path": str(file_path)
    }