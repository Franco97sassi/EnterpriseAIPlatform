from typing import Any

from qdrant_client import QdrantClient

from app.services.embedding_service import EmbeddingService


class QdrantRetrievalService:
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()

        self.client = QdrantClient(
            path="qdrant_rag_data"
        )

        self.collection_name = "rag_documents"

    def search(
        self,
        query: str,
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        if not query.strip():
            raise ValueError("Query cannot be empty")

        query_embedding = self.embedding_service.embed_text(query)

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            limit=limit,
            with_payload=True,
        )

        documents: list[dict[str, Any]] = []

        for point in results.points:
            payload = point.payload or {}

            documents.append(
                {
                    "id": str(point.id),
                    "score": float(point.score),
                    "source": payload.get("source"),
                    "chunk_index": payload.get("chunk_index"),
                    "text": payload.get("text"),
                }
            )

        return documents