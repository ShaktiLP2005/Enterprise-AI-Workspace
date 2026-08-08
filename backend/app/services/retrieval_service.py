from app.core.config import settings
from app.services.embedding_service import generate_query_embedding
from app.services.vector_store_service import search_embeddings
from app.services.generation_service import decompose_query


def retrieve_documents(
    query: str,
):
    """
    Retrieve relevant document chunks.

    Multiple independent questions are retrieved separately
    so that one question cannot dominate another during retrieval.
    """

    # Decompose the query into independent questions
    questions = decompose_query(query)

    all_results = []

    # Retrieve separately for every question
    for question in questions:

        # Generate embedding for this question
        query_embedding = generate_query_embedding(question)

        # Search ChromaDB
        search_results = search_embeddings(
            query_embedding=query_embedding,
            top_k=settings.PER_QUERY_TOP_K
        )

        # Keep all results for this question
        for chunk_id, chunk, metadata, distance in zip(
            search_results["ids"][0],
            search_results["documents"][0],
            search_results["metadatas"][0],
            search_results["distances"][0]
        ):
            all_results.append(
                {
                    "id": chunk_id,
                    "chunk": chunk,
                    "metadata": metadata,
                    "distance": distance
                }
            )

    # Remove duplicate chunks while preserving results
    # from every independent question
    unique_results = {}

    for result in all_results:

        if result["id"] not in unique_results:
            unique_results[result["id"]] = result

    results = list(unique_results.values())

    return {
        "query": query,
        "chunks": [
            result["chunk"]
            for result in results
        ],
        "metadata": [
            result["metadata"]
            for result in results
        ],
        "distances": [
            result["distance"]
            for result in results
        ],
        "ids": [
            result["id"]
            for result in results
        ]
    }