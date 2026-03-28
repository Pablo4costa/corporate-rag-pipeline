from dotenv import load_dotenv
load_dotenv()

import os
import asyncpg
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_connection():
    return await asyncpg.connect(os.getenv("DATABASE_URL"))

async def setup_database():
    conn = await get_connection()
    await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            embedding vector(1536),
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    await conn.close()

def get_embedding(text: str) -> list:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

async def embed_and_store(filename: str, chunks: list) -> int:
    conn = await get_connection()

    # Borrar chunks anteriores del mismo archivo
    await conn.execute(
        "DELETE FROM documents WHERE filename = $1", filename
    )

    stored = 0
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk.page_content)
        embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
        await conn.execute(
            """INSERT INTO documents (filename, chunk_index, content, embedding)
               VALUES ($1, $2, $3, $4::vector)""",
            filename, i, chunk.page_content, embedding_str
        )
        stored += 1

    await conn.close()
    return stored