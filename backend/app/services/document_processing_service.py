from fastapi import UploadFile

from app.services.document_service import save_document
from app.services.text_extraction_service import extract_text
from app.services.text_cleaning_service import clean_text
from app.services.chunking_service import chunk_text
from app.services.rag_ingestion_service import ingest_document


def process_document(file: UploadFile) -> dict:
    """
    Process an uploaded document from start to finish.
    """

    # Save document and generate its identity
    document = save_document(file)

    document_id = document["document_id"]
    filename = document["filename"]
    path = document["path"]

    # Extract raw text
    raw_text = extract_text(path)

    # Clean extracted text
    cleaned_text = clean_text(raw_text)

    # Split text into chunks
    chunks = chunk_text(cleaned_text)

    # Build document metadata
    metadata = {
        "document_id": document_id,
        "filename": filename
    }

    # Generate embeddings and store them
    ingestion_result = ingest_document(
        chunks=chunks,
        metadata=metadata
    )

    return {
        "message": "Document uploaded and ingested successfully.",
        "document_id": document_id,
        "filename": filename,
        "path": path,
        "total_chunks": len(chunks),
        "collection": ingestion_result["collection"]
    }