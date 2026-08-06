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