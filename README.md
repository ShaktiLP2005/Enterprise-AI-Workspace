# 🤖 Enterprise AI Workspace

>> **An end-to-end multi-document Retrieval-Augmented Generation (RAG) platform built with FastAPI, ChromaDB, FastEmbed, BGE embeddings, Groq, Docker, and a lightweight web frontend.**

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Project Highlights](#-project-highlights)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Architecture](#-architecture)
- [RAG Pipeline](#-rag-pipeline)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Run Locally](#-run-locally)
- [Run with Docker](#-run-with-docker)
- [API Endpoints](#-api-endpoints)
- [Example Queries](#-example-queries)
- [Deployment](#-deployment)
- [Current Capabilities](#-current-capabilities)
- [Future Roadmap](#-future-roadmap)
- [Author](#-author)
- [License](#-license)

---

## 📌 Overview

Enterprise AI Workspace is an end-to-end **Retrieval-Augmented Generation (RAG)** platform that allows users to upload multiple PDF documents and ask natural-language questions across their combined knowledge base.

The system processes uploaded documents through a complete ingestion pipeline:

**Document Upload → Text Extraction → Cleaning → Chunking → Embeddings → ChromaDB**

When a user asks a question, the system performs:

**Query Embedding → Semantic Retrieval → Context Construction → LLM Generation → Answer + Sources**

The platform supports **multi-document retrieval**, allowing information from different uploaded documents to be combined when answering a single query.

---

## ⭐ Project Highlights

- End-to-end multi-document RAG pipeline
- Multiple PDF upload and ingestion
- Semantic vector search using ChromaDB
- BGE embeddings using FastEmbed
- Query decomposition for multi-part questions
- LLM-powered answer generation using Groq
- Source attribution with retrieved document metadata
- Persistent document and vector storage
- FastAPI backend
- Lightweight web frontend
- Dockerized backend and frontend
- Docker Compose orchestration
- Nginx reverse proxy
- CORS-enabled frontend/backend communication
- Interactive API documentation through Swagger UI
- Production deployment on Render

---

## 🌐 Live Demo

🚀 **Try the application here**

👉 **[Launch Enterprise AI Workspace](https://enterprise-ai-workspace-frontend.onrender.com)**

> **Note**
>
> The hosted application is intended primarily as a demonstration environment.
> Depending on the hosting platform and instance inactivity, the first request may take some time while the service starts.

---

## ✨ Features

### 📄 Multi-Document Upload

Upload multiple PDF documents through the web interface.

Each document receives a unique document ID and is processed independently through the ingestion pipeline.

### 🧹 Document Processing

Uploaded documents go through:

- Text extraction
- Text cleaning
- Recursive chunking
- Embedding generation

### 🧠 Semantic Search

Questions are converted into embeddings and searched against document embeddings stored in ChromaDB.

### 📚 Cross-Document Question Answering

The system can retrieve information from multiple documents for a single query.

For example:

> What projects has Shakti built and what are the software installation instructions?

The system can retrieve the relevant information from multiple documents and generate a combined answer.

### 🧩 Query Decomposition

Complex queries containing multiple independent information requests can be decomposed into standalone questions before retrieval.

### 🤖 LLM Generation

Retrieved document chunks are provided as context to a Groq-hosted LLM which generates the final answer.

### 🔎 Source Attribution

Responses include the retrieved document sources, including:

- Document filename
- Chunk ID
- Retrieval distance

### 💾 Persistent Storage

Uploaded documents and ChromaDB data are stored using persistent storage when running locally with Docker Compose.

### 🐳 Dockerized Architecture

Both the FastAPI backend and frontend are containerized and can be orchestrated using Docker Compose.

### 🌐 Production Deployment

The application is deployed using separate frontend and backend services.

The frontend is served through Nginx and communicates with the deployed FastAPI backend over HTTPS.

---

## 🖼️ Screenshots

### 🏠 Home / Document Upload

The web interface allows users to upload one or more PDF documents and query the resulting knowledge base.

![Home / Document Upload](assets/home.png)

---

### 📄 Multiple Document Upload

Multiple PDF documents can be uploaded and ingested into the same knowledge base.

![Multiple Document Upload](assets/upload.png)

---

### 💬 Question Answering

Users can ask natural-language questions against the uploaded documents.

![Question Answering](assets/query.png)

---

### 📚 Cross-Document Question Answering

The system can combine information retrieved from multiple documents to answer a single question.

For example:

> **What projects has Shakti built and what are the software installation instructions?**

The system retrieves the relevant information from the appropriate documents and generates a combined answer.

![Cross-Document Answer](assets/sources1.png)

![Cross-Document Answer Sources](assets/sources2.png)

---

### 🔎 Source Attribution

Each generated response includes the document chunks used during retrieval, along with their similarity distances and source filenames.

This provides visibility into **which documents contributed to the generated answer**.

![Retrieved Sources](assets/sources2.png)

---

### 📖 API Documentation

The backend exposes an interactive Swagger UI through FastAPI.

![Swagger API Documentation](assets/swagger.png)

---

## 🏗️ Architecture

### System Architecture

```text
                           ┌───────────────────────────┐
                           │          User             │
                           │        Browser            │
                           └─────────────┬─────────────┘
                                         │
                                         │ HTTPS
                                         ▼
                           ┌───────────────────────────┐
                           │      Web Frontend         │
                           │   HTML / CSS / JavaScript │
                           └─────────────┬─────────────┘
                                         │
                                         │ /api/*
                                         ▼
                           ┌───────────────────────────┐
                           │          Nginx             │
                           │    Reverse Proxy / Web     │
                           └─────────────┬─────────────┘
                                         │
                                         │ HTTPS
                                         ▼
                    ┌────────────────────────────────────────┐
                    │              FastAPI Backend            │
                    │                                        │
                    │  Upload API │ Query API │ Health API   │
                    └──────────────┬─────────────────────────┘
                                   │
                  ┌────────────────┼────────────────┐
                  │                │                │
                  ▼                ▼                ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │    Document    │ │   Embedding    │ │   Retrieval    │
        │   Processing   │ │    Service     │ │    Service     │
        ├────────────────┤ ├────────────────┤ ├────────────────┤
        │ Text Extraction│ │   FastEmbed    │ │ Query Embedding│
        │ Text Cleaning  │ │ BGE Embeddings │ │ Semantic Search│
        │ Chunking       │ │                │ │ Top-K Retrieval│
        └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
                │                  │                  │
                │                  │                  ▼
                │                  │          ┌────────────────┐
                │                  └─────────►│    ChromaDB    │
                │                             │ Vector Store   │
                │                             └───────┬────────┘
                │                                     │
                │                                     │ Retrieved Context
                │                                     ▼
                │                             ┌────────────────┐
                └────────────────────────────►│ RAG Context   │
                                              │ Construction   │
                                              └───────┬────────┘
                                                      │
                                                      ▼
                                              ┌────────────────┐
                                              │    Groq LLM    │
                                              │ Answer Generate│
                                              └───────┬────────┘
                                                      │
                                                      ▼
                                              ┌────────────────┐
                                              │ Answer +       │
                                              │ Sources        │
                                              └───────┬────────┘
                                                      │
                                                      ▼
                                                ┌───────────┐
                                                │  Browser  │
                                                └──────
                                              ─────┘


---

## 🛠️ Tech Stack

### Backend

- **Python 3.12**
- **FastAPI** — REST API framework
- **Uvicorn** — ASGI server
- **PyMuPDF** — PDF text extraction
- **Pydantic** — Configuration and data validation

### RAG & AI

- **FastEmbed** — Efficient embedding generation
- **BAAI/bge-small-en-v1.5** — 384-dimensional text embeddings
- **ChromaDB** — Vector database and semantic retrieval
- **Groq** — LLM inference and answer generation
- **ONNX Runtime** — Local inference backend used by FastEmbed

### Frontend

- **HTML5**
- **CSS3**
- **JavaScript**
- **Nginx** — Static file serving and reverse proxy

### DevOps & Deployment

- **Docker**
- **Docker Compose**
- **Render** — Production deployment
- **Git & GitHub** — Version control and source hosting

### Architecture

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Web Server | Nginx |
| Backend API | FastAPI + Uvicorn |
| Document Processing | PyMuPDF |
| Text Embeddings | FastEmbed + BGE |
| Embedding Model | `BAAI/bge-small-en-v1.5` |
| Vector Database | ChromaDB |
| LLM Inference | Groq |
| Containerization | Docker + Docker Compose |
| Deployment | Render |
| Version Control | Git + GitHub |

---

## 🔄 RAG Pipeline

### 📥 Document Ingestion Pipeline

```text
PDF Upload
    │
    ▼
Document Storage
    │
    ▼
Text Extraction
    │
    ▼
Text Cleaning
    │
    ▼
Recursive Chunking
    │
    ▼
FastEmbed
(BGE Embeddings)
    │
    ▼
ChromaDB
(Vector Storage)

---

###📤 Query & Answer Pipeline

User Question
      │
      ▼
Query Decomposition
      │
      ▼
Query Embedding
      │
      ▼
ChromaDB Semantic Search
      │
      ▼
Relevant Document Chunks
      │
      ▼
Context Construction
      │
      ▼
Groq LLM
      │
      ▼
Generated Answer
      │
      ▼
Source Attribution

---

## 📁 Project Structure

```text
Enterprise-AI-Workspace/
│
├── backend/
│   └── app/
│       ├── api/
│       │   ├── upload.py
│       │   ├── query.py
│       │   └── health.py
│       │
│       ├── core/
│       │   └── config.py
│       │
│       ├── services/
│       │   ├── document_service.py
│       │   ├── document_processing_service.py
│       │   ├── text_extraction_service.py
│       │   ├── text_cleaning_service.py
│       │   ├── chunking_service.py
│       │   ├── embedding_service.py
│       │   ├── rag_ingestion_service.py
│       │   ├── rag_query_service.py
│       │   └── vector_store_service.py
│       │
│       └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── assets/
│   ├── home.png
│   ├── upload.png
│   ├── query.png
│   ├── sources1.png
│   ├── sources2.png
│   └── swagger.png
│
├── data/
│   └── uploads/
│
├── chroma_db/
│
├── docker/
│   ├── Dockerfile
│   ├── frontend.Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml
├── requirements.txt
└── README.md

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ShaktiLP2005/Enterprise-AI-Workspace.git
cd Enterprise-AI-Workspace
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create the environment file:

```text
backend/.env
```

Add the required environment variables, including the Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

> **Never commit API keys, `.env` files, or other secrets to GitHub.**

---

## ▶️ Run Locally

### 1. Start the Backend

From the project root:

```powershell
uvicorn app.main:app --app-dir backend --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

### 2. Start the Frontend

Open a second terminal and run:

```powershell
cd frontend
python -m http.server 3000
```

The frontend will be available at:

```text
http://127.0.0.1:3000
```

### 3. API Documentation

FastAPI provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

The Swagger UI can be used to test the available backend endpoints directly.

---

## 🐳 Run with Docker

### 1. Build and Start the Services

From the project root:

```bash
docker compose up --build
```

This starts both:

- **Backend** — FastAPI + Uvicorn
- **Frontend** — Nginx + static web application

### 2. Run in the Background

```bash
docker compose up --build -d
```

### 3. Access the Application

Frontend:

```text
http://localhost:3000
```

Backend:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

### 4. Stop the Services

```bash
docker compose down
```

### 5. Persistent Storage

Docker Compose mounts persistent storage for uploaded documents and ChromaDB:

```text
./data/uploads → /app/data/uploads
./chroma_db    → /app/chroma_db
```

This allows uploaded documents and vector database data to persist across container restarts.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check backend health status |
| `POST` | `/upload/` | Upload and ingest one or more PDF documents |
| `POST` | `/query/` | Ask a question against the document knowledge base |
| `GET` | `/docs` | Open interactive Swagger API documentation |

### 📄 Upload Documents

```http
POST /upload/
```

Accepts one or more PDF files and processes them through the complete ingestion pipeline.

Example using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/upload/ \
  -F "files=@document.pdf"
```

### 💬 Query Documents

```http
POST /query/
```

Accepts a natural-language question and returns an answer generated from the retrieved document context.

### ❤️ Health Check

```http
GET /health
```

Returns the current health status of the backend service.

### 📖 Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

FastAPI automatically provides an interactive interface for exploring and testing the available API endpoints.

---

## 💬 Example Queries

Users can ask natural-language questions about the documents that have been uploaded to the knowledge base.

### 📄 Single-Document Queries

```text
What is Shakti's CGPA?
```

```text
What projects has Shakti built?
```

```text
What technologies were used in the projects?
```

```text
What are the software installation instructions?
```

### 📚 Cross-Document Query

The system can combine information retrieved from multiple documents to answer a single question.

Example:

```text
What projects has Shakti built and what are the software installation instructions?
```

The query can retrieve relevant information from different documents and generate a combined answer with source attribution.

### 🔎 Source-Aware Answers

Generated answers include information about the retrieved sources, such as:

- Source document filename
- Retrieved document chunk
- Retrieval distance

This makes it possible to inspect which documents contributed to the generated response.

---

## 🚀 Deployment

### Production Architecture

```text
                         ┌──────────────────────┐
                         │     User Browser     │
                         └──────────┬───────────┘
                                    │
                                  HTTPS
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Render Frontend    │
                         │  Nginx + Static UI   │
                         └──────────┬───────────┘
                                    │
                              HTTPS Proxy
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Render Backend     │
                         │ FastAPI + Uvicorn    │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
          ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
          │   FastEmbed  │   │   ChromaDB   │   │   Groq LLM   │
          │ BGE Embedding│   │ Vector Store │   │  Generation  │
          └──────────────┘   └──────────────┘   └──────────────┘
```

### 🌐 Live Application

[Launch Enterprise AI Workspace](https://enterprise-ai-workspace-frontend.onrender.com)

> **Note:** The hosted application runs on Render. Depending on instance inactivity, the first request may take some time while the service starts.

### ☁️ Deployment Components

- **Frontend:** Nginx-based container deployed on Render
- **Backend:** FastAPI + Uvicorn deployed on Render
- **Reverse Proxy:** Nginx routes API requests from the frontend to the backend
- **Embeddings:** FastEmbed with `BAAI/bge-small-en-v1.5`
- **Vector Store:** ChromaDB
- **LLM:** Groq
- **Source Repository:** GitHub

---

## ✅ Current Capabilities

- [x] Multi-document PDF upload
- [x] PDF text extraction
- [x] Text cleaning
- [x] Recursive text chunking
- [x] BGE embedding generation
- [x] Batch embedding generation for reduced memory usage
- [x] Semantic vector search
- [x] ChromaDB vector storage
- [x] Cross-document retrieval
- [x] Query decomposition
- [x] Groq-powered answer generation
- [x] Source attribution
- [x] Document metadata tracking
- [x] FastAPI REST API
- [x] Interactive Swagger documentation
- [x] Nginx reverse proxy
- [x] Dockerized backend
- [x] Dockerized frontend
- [x] Docker Compose orchestration
- [x] Production deployment on Render
- [x] Live web application

---

## 🔮 Future Roadmap

- [ ] Streaming LLM responses
- [ ] Conversation history
- [ ] User authentication
- [ ] Per-user knowledge bases
- [ ] Document-specific querying
- [ ] Support for additional document formats
- [ ] Hybrid keyword + semantic search
- [ ] Retrieval reranking
- [ ] Retrieval evaluation
- [ ] Answer-quality evaluation
- [ ] Background processing for large documents
- [ ] Production-grade persistent vector storage
- [ ] Monitoring and observability
- [ ] Improved UI/UX

---

## 👨‍💻 Author

**Shakti Prasanna Dash**

Computer Science Student

- GitHub: [ShaktiLP2005](https://github.com/ShaktiLP2005)

---

## 📄 License

This project is intended for educational and portfolio purposes.

If you plan to distribute or reuse the project, add an appropriate open-source license such as the **MIT License**.
