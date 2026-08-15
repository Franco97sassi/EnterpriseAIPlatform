from app.services.document_loader import DocumentLoader


loader = DocumentLoader()

text = loader.load_pdf("data/test.pdf")

print("Characters extracted:", len(text))
print("\nFirst 500 characters:")
print(text[:500])