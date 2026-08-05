import fitz  # PyMuPDF


def extract_text(file_path: str) -> str:
    """
    Extract all text from a PDF document.
    """

    try:
        # Open the PDF document
        document = fitz.open(file_path)

        extracted_text = ""

        # Read every page
        for page in document:
            extracted_text += page.get_text()

        # Close the document
        document.close()

        return extracted_text

    except Exception as error:
        raise RuntimeError(f"Failed to extract text: {error}")