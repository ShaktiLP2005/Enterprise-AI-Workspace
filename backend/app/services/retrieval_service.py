from app.core.config import settings
from app.services.embedding_service import generate_query_embedding
from app.services.vector_store_service import search_embeddings


def retrieve_documents(
    query: str,
):
    """
    Retrieve the most relevant document chunks.
    """

    # Generate query embedding
    query_embedding = generate_query_embedding(query)

    # Search ChromaDB
    results = search_embeddings(
        query_embedding=query_embedding,
        top_k=settings.TOP_K
    )

    return {
        "query": query,
        "chunks": results["documents"][0],
        "metadata": results["metadatas"][0]
    }