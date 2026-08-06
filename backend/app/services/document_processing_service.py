from pathlib import Path

from fastapi import UploadFile

from app.services.document_service import save_document
from app.services.text_extraction_service import extract_text
from app.services.text_cleaning_service import clean_text
from app.services.chunking_service import chunk_text


def process_document(file: UploadFile) -> dict:
    """
    Process an uploaded document from start to finish.
    """

    # Save uploaded document
    path = save_document(file)

    # Extract raw text
    raw_text = extract_text(path)

    # Clean extracted text
    cleaned_text = clean_text(raw_text)

    # Split text into chunks
    chunks = chunk_text(cleaned_text)

    # Build document metadata
    metadata = {
        "filename": Path(path).name
    }

    return {
        "path": path,
        "chunks": chunks,
        "metadata": metadata
    }