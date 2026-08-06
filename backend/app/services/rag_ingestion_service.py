from app.services.embedding_service import generate_embeddings
from app.services.vector_store_service import store_embeddings


def ingest_document(
    chunks: list[str],
    metadata: dict
):
    """
    Generate embeddings and store them in the vector database.
    """

    # Generate embeddings for every chunk
    embeddings = generate_embeddings(chunks)

    # Store chunks and embeddings in ChromaDB
    result = store_embeddings(
        chunks=chunks,
        embeddings=embeddings,
        metadata=metadata
    )

    return result