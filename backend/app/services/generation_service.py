from openai import OpenAI

from app.core.config import settings
from app.prompts.rag_prompt import RAG_PROMPT


# Create the Groq client
client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def generate_answer(
    question: str,
    chunks: list[str]
) -> str:
    """
    Generate an answer using the retrieved document chunks.
    """

    try:

        # Combine retrieved chunks into one context
        context = "\n\n".join(chunks)

        # Build the final prompt
        prompt = RAG_PROMPT.format(
            context=context,
            question=question
        )

        # Generate a response
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
           messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant that answers questions "
                        "using only the provided document context."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception as error:
        raise RuntimeError(
            f"Failed to generate answer: {error}"
        )


def decompose_query(query: str) -> list[str]:
    """
    Determine whether a user query contains multiple independent questions.

    Returns a list of standalone questions.
    """

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a query decomposition assistant for a RAG system. "
                        "Determine whether the user's query contains multiple independent "
                        "information requests.\n\n"

                        "If it contains only one information request, return "
                        "the original query as a single item.\n\n"

                        "If it contains multiple independent requests, split "
                        "them into separate standalone questions.\n\n"

                        "Do NOT split a single related request into multiple questions. "
                        "For example, a question asking about a project and its technologies "
                        "should remain one question.\n\n"

                        "Each returned question must be self-contained and understandable "
                        "without the original query.\n\n"

                        "Return ONLY the questions, one per line. "
                        "Do not number them. "
                        "Do not add explanations."
                    )
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        questions = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

        if not questions:
            return [query]

        print("\nDecomposed questions:")

        for question in questions:
            print(f"- {question}")

        return questions

    except Exception:
        # Retrieval should still work if decomposition fails
        return [query]