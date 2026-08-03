from pathlib import Path
import shutil

# Directory where uploaded files will be stored
UPLOAD_DIR = Path("data/uploads")

# Create the directory if it doesn't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_document(file):
    # Build the complete file path
    file_path = UPLOAD_DIR / file.filename

    # Save the uploaded file in binary mode
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Return the saved file path
    return str(file_path)