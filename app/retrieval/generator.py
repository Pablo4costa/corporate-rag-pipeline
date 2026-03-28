from dotenv import load_dotenv
load_dotenv()

import os
from openai import OpenAI
from app.retrieval.search import semantic_search

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_answer(query: str) -> dict:
    # Buscar chunks relevantes
    chunks = await semantic_search(query, limit=5)

    if not chunks:
        return {
            "answer": "No relevant documents found to answer your question.",
            "sources": []
        }

    # Construir contexto con los chunks encontrados
    context = "\n\n".join([
        f"[Source: {chunk['filename']} | Similarity: {chunk['similarity']:.2f}]\n{chunk['content']}"
        for chunk in chunks
    ])

    # Prompt con contexto inyectado
    system_prompt = """You are a helpful assistant that answers questions based strictly on the provided documents.
If the answer is not found in the documents, say so clearly.
Always cite which document you got the information from."""

    user_prompt = f"""Based on the following documents, answer this question: {query}

Documents:
{context}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    answer = response.choices[0].message.content

    # Fuentes únicas utilizadas
    sources = list(set([chunk["filename"] for chunk in chunks]))

    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": len(chunks)
    }