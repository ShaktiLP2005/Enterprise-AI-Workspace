from pathlib import Path
import shutil

# Get the absolute path of this file
CURRENT_FILE = Path(__file__).resolve()

# Navigate to the project root
# document_service.py -> services -> app -> backend -> Enterprise-AI-Workspace
PROJECT_ROOT = CURRENT_FILE.parents[3]

# Directory where uploaded files will be stored
UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"

# Create the directory if it doesn't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_document(file):
    # Build the complete destination path
    file_path = UPLOAD_DIR / file.filename

    # Save the uploaded file in binary mode
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Return the saved file path
    return str(file_path)