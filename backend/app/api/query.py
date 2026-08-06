from fastapi import APIRouter

from app.services.retrieval_service import retrieve_documents
from app.services.generation_service import generate_answer

router = APIRouter(
    prefix="/query",
    tags=["Retrieval"]
)


@router.post("/")
def query_documents(query: str):
    """
    Retrieve relevant document chunks and generate an answer.
    """

    # Retrieve relevant chunks
    retrieved = retrieve_documents(query)

    # Generate answer
    answer = generate_answer(
        question=query,
        chunks=retrieved["chunks"]
    )

    return {
        "query": query,
        "answer": answer,
        "retrieved_chunks": retrieved["chunks"]
    }