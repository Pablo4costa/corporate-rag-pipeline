# Corporate RAG Pipeline 📄🔍

A production-ready document ingestion and semantic search pipeline for corporate environments, with CI/CD automation via GitHub Actions.

## Overview

Enterprises have vast amounts of internal documentation — policies, manuals, reports — that are hard to search and query. This pipeline ingests corporate documents and allows teams to ask questions in natural language, getting precise answers with source citations.

## Architecture
```
Documents (PDF, TXT, DOCX)
        ↓
   Document Loader
        ↓
   Text Splitter (chunks)
        ↓
   Embeddings (OpenAI)
        ↓
   PostgreSQL + pgvector
        ↓
   Semantic Search
        ↓
   LLM (GPT-4o-mini)
        ↓
   Answer + Sources
```

## Features

- 📄 **Multi-format ingestion** — supports PDF, TXT and DOCX files
- 🔍 **Semantic search** — finds relevant content by meaning, not just keywords
- 🤖 **AI-powered answers** — generates precise responses with source citations
- 🚀 **REST API** — clean FastAPI interface with auto-generated docs
- 🐳 **Docker ready** — full stack runs with a single command
- ⚙️ **CI/CD** — automated tests on every push via GitHub Actions
- 🔒 **Secure** — API keys managed via environment variables

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI + Uvicorn |
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector Database | PostgreSQL 16 + pgvector |
| Document Processing | LangChain + LangChain Community |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |

## Getting Started

### Prerequisites

- Python 3.11+
- Docker Desktop
- OpenAI API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/Pablo4costa/corporate-rag-pipeline.git
cd corporate-rag-pipeline
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Linux/Mac
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. Start infrastructure
```bash
docker compose up -d
```

6. Start the server
```bash
uvicorn app.main:app --reload
```

7. Open API docs
```
http://127.0.0.1:8000/docs
```

## API Endpoints

### POST /api/v1/upload
Upload and index a document.
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@your-document.pdf"
```

### POST /api/v1/query
Ask a question about your documents.
```json
{
  "question": "How many vacation days do full-time employees get?"
}
```

Response:
```json
{
  "answer": "Full-time employees are entitled to 15 days of paid vacation per year. (Source: hr-policy.txt)",
  "sources": ["hr-policy.txt"],
  "chunks_used": 1
}
```

### GET /api/v1/documents
List all indexed documents.

## How It Works

1. **Upload** — document is loaded and split into chunks of 500 characters
2. **Embed** — each chunk is converted to a vector using OpenAI embeddings
3. **Store** — vectors are stored in PostgreSQL with pgvector extension
4. **Query** — user question is embedded and compared against stored vectors
5. **Generate** — top matching chunks are sent to GPT-4o-mini with the question
6. **Answer** — response is returned with source citations

## CI/CD Pipeline

Every push to `main` triggers the GitHub Actions pipeline:
- Sets up Python 3.11
- Installs all dependencies
- Runs automated tests

## Project Structure
```
corporate-rag-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── .env.example
├── README.md
├── requirements.txt
├── pytest.ini
├── app/
│   ├── main.py
│   ├── ingestion/
│   │   ├── loader.py
│   │   └── embedder.py
│   ├── retrieval/
│   │   ├── search.py
│   │   └── generator.py
│   └── api/
│       └── routes.py
└── tests/
    └── test_rag.py
```

## License

MIT