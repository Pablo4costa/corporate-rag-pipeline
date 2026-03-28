from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.ingestion.loader import load_document
from app.ingestion.embedder import setup_database, embed_and_store
from app.retrieval.generator import generate_answer
import tempfile
import os

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list
    chunks_used: int

@router.on_event("startup")
async def startup():
    await setup_database()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Guardar archivo temporalmente
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Procesar e indexar
        chunks = load_document(tmp_path)
        stored = await embed_and_store(file.filename, chunks)

        # Limpiar archivo temporal
        os.unlink(tmp_path)

        return {
            "filename": file.filename,
            "chunks_indexed": stored,
            "message": "Document uploaded and indexed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        result = await generate_answer(request.question)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def list_documents():
    try:
        from app.ingestion.embedder import get_connection
        conn = await get_connection()
        rows = await conn.fetch(
            "SELECT filename, COUNT(*) as chunks FROM documents GROUP BY filename"
        )
        await conn.close()
        return {"documents": [dict(row) for row in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))