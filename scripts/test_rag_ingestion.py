from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.services.document_loader import DocumentLoader
from app.services.embedding_service import EmbeddingService
from app.services.text_chunker import TextChunker


loader = DocumentLoader()
chunker = TextChunker(
    chunk_size=500,
    chunk_overlap=100,
)
embedding_service = EmbeddingService()

client = QdrantClient(path="qdrant_rag_data")

collection_name = "rag_documents"

try:
    text = loader.load_pdf("data/test.pdf")

    chunks = chunker.split_text(text)

    embeddings = embedding_service.embed_texts(chunks)

    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

    points = [
        PointStruct(
            id=index,
            vector=embedding.tolist(),
            payload={
                "text": chunk,
                "source": "test.pdf",
                "chunk_index": index,
            },
        )
        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        )
    ]

    client.upsert(
        collection_name=collection_name,
        points=points,
    )

    print("Chunks stored:", len(points))

finally:
    client.close()