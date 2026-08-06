from pathlib import Path

import chromadb


# Get the absolute path of this file
CURRENT_FILE = Path(__file__).resolve()

# Navigate to the project root
PROJECT_ROOT = CURRENT_FILE.parents[3]

# Directory where ChromaDB stores its data
CHROMA_DB_DIR = PROJECT_ROOT / "chroma_db"

# Collection name for storing document embeddings
COLLECTION_NAME = "documents"


# Create a persistent ChromaDB client
client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))

# Create the collection if it doesn't already exist
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
    """

    try:
        # Get the ChromaDB collection
        collection = get_collection()

        # Generate a unique ID for every chunk
        ids = [
            f"{metadata['filename']}_chunk_{index + 1}"
            for index in range(len(chunks))
        ]

        # Duplicate metadata for every chunk
        metadatas = [
            metadata.copy()
            for _ in chunks
        ]

        # Store everything in ChromaDB
        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return {
            "message": "Embeddings stored successfully.",
            "collection": COLLECTION_NAME,
            "chunks_stored": len(chunks)
        }

    except Exception as error:
        raise RuntimeError(f"Failed to store embeddings: {error}")

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