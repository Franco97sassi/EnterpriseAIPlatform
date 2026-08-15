from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.services.embedding_service import EmbeddingService


client = QdrantClient(path="qdrant_data")
embedding_service = EmbeddingService()

collection_name = "documents"

documents = [
    "Python is used for artificial intelligence.",
    "Machine learning is a branch of AI.",
    "I like eating pizza.",
]

try:
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

    embeddings = embedding_service.embed_texts(documents)

    points = [
        PointStruct(
            id=index,
            vector=embedding.tolist(),
            payload={"text": document},
        )
        for index, (document, embedding) in enumerate(
            zip(documents, embeddings)
        )
    ]

    client.upsert(
        collection_name=collection_name,
        points=points,
    )

    query = "Artificial intelligence with Python"
    query_embedding = embedding_service.embed_text(query)

    results = client.query_points(
        collection_name=collection_name,
        query=query_embedding.tolist(),
        limit=3,
        with_payload=True,
    )

    print("\nSemantic search results:")

    for point in results.points:
        print(
            f"{point.score:.4f} -> "
            f"{point.payload['text']}"
        )

finally:
    client.close()