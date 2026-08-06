from fastapi import APIRouter, UploadFile, File

from app.services.document_processing_service import process_document
from app.services.rag_ingestion_service import ingest_document


router = APIRouter(
    prefix="/upload",
    tags=["Document Upload"]
)


@router.post("/")
def upload_document(file: UploadFile = File(...)):
    """
    Upload, process, and ingest a document into the vector database.
    """

    # Process the uploaded document
    processed_document = process_document(file)

    # Ingest the processed document into ChromaDB
    ingestion_result = ingest_document(
        chunks=processed_document["chunks"],
        metadata=processed_document["metadata"]
    )

    return {
        "message": "Document uploaded and ingested successfully.",
        "path": processed_document["path"],
        "total_chunks": len(processed_document["chunks"]),
        "collection": ingestion_result["collection"]
    }