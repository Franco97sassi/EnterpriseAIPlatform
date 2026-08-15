from app.services.embedding_service import EmbeddingService


service = EmbeddingService()

texts = [
    "Python is used for artificial intelligence.",
    "Machine learning is a branch of AI.",
    "I like eating pizza.",
]

embeddings = service.embed_texts(texts)

print("Shape:", embeddings.shape)
print("First vector size:", len(embeddings[0]))