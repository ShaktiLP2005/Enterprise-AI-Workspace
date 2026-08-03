from fastapi import FastAPI

from app.api import upload

app = FastAPI(
    title="Enterprise AI Workspace",
    description="Enterprise RAG Platform",
    version="1.0.0"
)

app.include_router(upload.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Enterprise AI Workspace"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }