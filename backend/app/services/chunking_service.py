from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text: str) -> list[str]:
    """
    Split cleaned text into overlapping chunks.
    """

    # Configure recursive chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
    )

    # Generate chunks
    chunks = splitter.split_text(text)

    return chunks