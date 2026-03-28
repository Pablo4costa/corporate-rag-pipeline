from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.routes import router

load_dotenv()

app = FastAPI(
    title="Corporate RAG Pipeline",
    description="Document ingestion and semantic search pipeline for corporate environments",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}