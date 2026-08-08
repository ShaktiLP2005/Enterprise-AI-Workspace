# Enterprise AI Workspace

A Dockerized multi-document Retrieval-Augmented Generation (RAG) platform that allows users to upload PDF documents, search their combined knowledge base using semantic retrieval, and ask natural-language questions using an LLM.

## Status

✅ Core RAG pipeline complete
✅ Multi-document ingestion
✅ Semantic retrieval
✅ Cross-document question answering
✅ Persistent vector storage
✅ Dockerized backend and frontend

---

## Overview

Enterprise AI Workspace is an end-to-end RAG application designed around a simple workflow:

1. Upload one or more PDF documents.
2. Extract and clean their text.
3. Split the text into overlapping chunks.
4. Generate embeddings for each chunk.
5. Store the embeddings and metadata in ChromaDB.
6. Ask natural-language questions.
7. Retrieve the most relevant chunks across all uploaded documents.
8. Generate an answer using the retrieved context and an LLM.
9. Display the answer together with its source documents.

The system supports questions that require information from multiple documents.

For example:

> What is Shakti's CGPA and what are the software installation instructions?

The system can retrieve the relevant information from different documents and combine it into a single answer.

---

## Architecture

```text
                         ┌─────────────────────┐
                         │       Browser       │
                         │     Frontend UI     │
                         │      Nginx :3000    │
                         └──────────┬──────────┘
                                    │
                              HTTP Requests
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       FastAPI       │
                         │      Backend        │
                         │       :8000         │
                         └──────────┬──────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
          Document Pipeline     Retrieval          Generation
                 │                  │                  │
                 ▼                  ▼                  ▼
          Text Extraction      Query Embedding      Groq LLM
                 │                  │
                 ▼                  ▼
          Text Cleaning         ChromaDB
                 │                  │
                 ▼                  │
             Chunking ◄─────────────┘
                 │
                 ▼
             Embeddings
                 │
                 ▼
             ChromaDB