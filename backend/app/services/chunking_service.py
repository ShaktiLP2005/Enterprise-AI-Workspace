from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text: str) -> list[str]:
    """
    Split cleaned text into overlapping chunks.
    """

    # Configure recursive chunking with a better separator hierarchy
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ],
        length_function=len,
    )

    # Generate chunks
    chunks = splitter.split_text(text)

    return chunks