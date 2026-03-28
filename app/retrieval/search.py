from dotenv import load_dotenv
load_dotenv()

import os
import asyncpg
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_connection():
    return await asyncpg.connect(os.getenv("DATABASE_URL"))

def get_embedding(text: str) -> list:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

async def semantic_search(query: str, limit: int = 5) -> list:
    embedding = get_embedding(query)
    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"

    conn = await get_connection()
    rows = await conn.fetch(
        """SELECT filename, content, chunk_index,
           1 - (embedding <=> $1::vector) AS similarity
           FROM documents
           ORDER BY embedding <=> $1::vector
           LIMIT $2""",
        embedding_str, limit
    )
    await conn.close()

    return [
        {
            "filename": row["filename"],
            "content": row["content"],
            "chunk_index": row["chunk_index"],
            "similarity": float(row["similarity"])
        }
        for row in rows
    ]