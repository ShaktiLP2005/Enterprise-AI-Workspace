from fastapi import APIRouter, HTTPException

from app.services.retrieval_service import retrieve_documents
from app.services.generation_service import generate_answer


router = APIRouter(
    prefix="/query",
    tags=["RAG Query"]
)


@router.post("/")
def query_documents(query: str):
    """
    Retrieve relevant document chunks and generate an answer.
    """

    # Validate query
    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    try:
        # Retrieve relevant document chunks
        retrieval = retrieve_documents(query)

        # Generate answer using retrieved chunks
        answer = generate_answer(
            question=query,
            chunks=retrieval["chunks"]
        )

        # Build source information
        sources = [
            {
                "id": chunk_id,
                "distance": distance,
                "filename": metadata.get("filename")
            }
            for chunk_id, distance, metadata in zip(
                retrieval["ids"],
                retrieval["distances"],
                retrieval["metadata"]
            )
        ]

        return {
            "query": query,
            "answer": answer,
            "sources": sources
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {error}"
        )