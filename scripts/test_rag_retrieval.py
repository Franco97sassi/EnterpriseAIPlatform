from qdrant_client import QdrantClient

from app.services.embedding_service import EmbeddingService


embedding_service = EmbeddingService()
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

    print("\nQuery:")
    print(query)

    print("\nRetrieved chunks:")

    for point in results.points:
        print("\n---")
        print(f"Score: {point.score:.4f}")
        print(f"Source: {point.payload['source']}")
        print(f"Chunk: {point.payload['chunk_index']}")
        print(point.payload["text"])

finally:
    client.close()