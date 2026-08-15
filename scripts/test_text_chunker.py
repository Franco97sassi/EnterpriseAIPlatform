from app.services.document_loader import DocumentLoader
from app.services.text_chunker import TextChunker


loader = DocumentLoader()
chunker = TextChunker(
    chunk_size=500,
    chunk_overlap=100,
)

text = loader.load_pdf("data/test.pdf")

chunks = chunker.split_text(text)

print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks):
    print(f"\n--- Chunk {index + 1} ---")
    print(chunk)