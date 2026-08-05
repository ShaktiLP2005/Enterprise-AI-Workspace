import re


def clean_text(text: str) -> str:
    """
    Clean extracted document text before chunking.
    """

    # Remove leading and trailing whitespace
    text = text.strip()

    # Replace multiple spaces with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Replace multiple blank lines with two newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text