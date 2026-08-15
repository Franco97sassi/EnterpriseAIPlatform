from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

documents = [
    "Python is used for artificial intelligence.",
    "Machine learning is a branch of AI.",
    "I like eating pizza.",
]

query = "Artificial intelligence with Python"

document_embeddings = model.encode(documents)
query_embedding = model.encode(query)

scores = cos_sim(query_embedding, document_embeddings)[0]

for document, score in zip(documents, scores):
    print(f"{score.item():.4f} -> {document}")