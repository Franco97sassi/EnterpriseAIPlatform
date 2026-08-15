import asyncio

from qdrant_client import QdrantClient

from app.services.embedding_service import EmbeddingService
from app.services.gemini_provider import GeminiProvider


async def main() -> None:
    embedding_service = EmbeddingService()
    llm = GeminiProvider()
    client = QdrantClient(path="qdrant_rag_data")

    collection_name = "rag_documents"
    query = "What is RAG and what steps does it include?"

    try:
        query_embedding = embedding_service.embed_text(query)

        results = client.query_points(
            collection_name=collection_name,
            query=query_embedding.tolist(),
            limit=2,
            with_payload=True,
        )

        context = "\n\n".join(
            point.payload["text"]
            for point in results.points
        )

        prompt = f"""
Answer the question using only the context below.

If the answer is not contained in the context, say:
"I don't have enough information in the provided context."

Context:
{context}

Question:
{query}
"""

        response = await llm.generate(prompt)

        print("\nQuestion:")
        print(query)

        print("\nAnswer:")
        print(response)

        print("\nCitations:")

        for point in results.points:
            print(
                f"- {point.payload['source']} "
                f"(chunk {point.payload['chunk_index']}) "
                f"score={point.score:.4f}"
            )

    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())