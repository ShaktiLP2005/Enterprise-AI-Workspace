from fastapi import FastAPI

from app.api import upload, query

app = FastAPI(
    title="Enterprise AI Workspace",
    description="Enterprise RAG Platform",
    version="1.0.0"
)

# Register routers
app.include_router(upload.router)
app.include_router(query.router)


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