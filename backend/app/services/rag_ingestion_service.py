from app.services.embedding_service import generate_embeddings
from app.services.vector_store_service import (
    store_embeddings,
    delete_document_embeddings
)


BATCH_SIZE = 16


def ingest_document(
    chunks: list[str],
    metadata: dict
):
    """
    Generate embeddings and store them in ChromaDB in batches.
    """

    try:
        # Remove the previous version once, before inserting new chunks.
        delete_document_embeddings(
            filename=metadata["filename"]
        )

        total_chunks = len(chunks)

        for start in range(0, total_chunks, BATCH_SIZE):

            end = min(
                start + BATCH_SIZE,
                total_chunks
            )

            batch_chunks = chunks[start:end]

            embeddings = generate_embeddings(
                batch_chunks,
                batch_size=BATCH_SIZE
            )

            store_embeddings(
                chunks=batch_chunks,
                embeddings=embeddings,
                metadata=metadata,
                start_index=start
            )

        return {
            "message": "Embeddings stored successfully.",
            "collection": "documents",
            "document_id": metadata["document_id"],
            "filename": metadata["filename"],
            "chunks_stored": total_chunks
        }

    except Exception as error:
        raise RuntimeError(
            f"Failed to ingest document: {error}"
        )