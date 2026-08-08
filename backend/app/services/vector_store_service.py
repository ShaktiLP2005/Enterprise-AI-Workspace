from pathlib import Path

import chromadb

from app.core.config import settings


# Directory where ChromaDB stores its data
CHROMA_DB_DIR = Path(settings.CHROMA_DB_DIR)

# Create the directory if it doesn't exist
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

# Collection name for storing document embeddings
COLLECTION_NAME = "documents"


# Create a persistent ChromaDB client
client = chromadb.PersistentClient(
    path=str(CHROMA_DB_DIR)
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

def get_collection():
    """
    Return the ChromaDB collection.
    """

    return collection

def store_embeddings(
    chunks: list[str],
    embeddings: list[list[float]],
    metadata: dict
):
    """
    Store document chunks and embeddings in ChromaDB.

    If a document with the same filename already exists,
    its previous chunks are removed before storing the new version.
    """

    try:
        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match number of embeddings."
            )

        collection = get_collection()

        document_id = metadata["document_id"]
        filename = metadata["filename"]

        # Remove the previous version of the same document
        collection.delete(
            where={"filename": filename}
        )

        # Generate unique IDs for every chunk
        ids = [
            f"{document_id}_chunk_{index + 1}"
            for index in range(len(chunks))
        ]

        # Add chunk-specific metadata
        metadatas = [
            {
                **metadata,
                "chunk_index": index + 1
            }
            for index in range(len(chunks))
        ]

        # Store chunks, embeddings, and metadata
        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return {
            "message": "Embeddings stored successfully.",
            "collection": COLLECTION_NAME,
            "document_id": document_id,
            "filename": filename,
            "chunks_stored": len(chunks)
        }

    except Exception as error:
        raise RuntimeError(
            f"Failed to store embeddings: {error}"
        )

def search_embeddings(
    query_embedding: list[float],
    top_k: int = 3
):
    """
    Search ChromaDB for the most relevant document chunks.
    """

    try:
        collection = get_collection()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results

    except Exception as error:
        raise RuntimeError(f"Failed to search embeddings: {error}")