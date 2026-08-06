from sentence_transformers import SentenceTransformer

from app.core.config import settings

try:
    # Load the embedding model once when this module is imported
    model = SentenceTransformer(settings.EMBEDDING_MODEL)

except Exception as error:
    raise RuntimeError(f"Failed to load embedding model: {error}")


def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of document chunks.
    """

    try:
        # Convert every chunk into an embedding vector
        embeddings = model.encode(chunks)

        # Convert NumPy array to a regular Python list
        return embeddings.tolist()

    except Exception as error:
        raise RuntimeError(f"Failed to generate embeddings: {error}")


def generate_query_embedding(query: str) -> list[float]:
    """
    Generate an embedding for a user query.
    """

    try:
        # Convert the query into an embedding vector
        embedding = model.encode(query)

        # Convert NumPy array to a regular Python list
        return embedding.tolist()

    except Exception as error:
        raise RuntimeError(f"Failed to generate query embedding: {error}")