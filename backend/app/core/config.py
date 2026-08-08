from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Enterprise-AI-Workspace/
# └── backend/
#     └── app/
#         └── core/
#             └── config.py
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    GROQ_API_KEY: str
    GROQ_MODEL: str

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    PER_QUERY_TOP_K: int = 3

    UPLOAD_DIR: str = str(
        PROJECT_ROOT / "data" / "uploads"
    )

    CHROMA_DB_DIR: str = str(
        PROJECT_ROOT / "chroma_db"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()