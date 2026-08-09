from fastembed import TextEmbedding

from app.core.config import settings

try:
    # Load the embedding model once when this module is imported
    model = TextEmbedding(
        model_name=settings.EMBEDDING_MODEL
    )

except Exception as error:
    raise RuntimeError(
        f"Failed to load embedding model: {error}"
    )


def generate_embeddings(
    chunks: list[str],
    batch_size: int = 16
) -> list[list[float]]:
    """
    Generate embeddings for document chunks in batches.
    """

    try:
        embeddings = model.embed(
            chunks,
            batch_size=batch_size
        )

        return [
            embedding.tolist()
            for embedding in embeddings
        ]

    except Exception as error:
        raise RuntimeError(
            f"Failed to generate embeddings: {error}"
        )

def generate_query_embedding(
    query: str
) -> list[float]:
    """
    Generate an embedding for a user query.
    """

    try:
        embedding = next(
            model.embed([query])
        )

        return embedding.tolist()

    except Exception as error:
        raise RuntimeError(
            f"Failed to generate query embedding: {error}"
        )