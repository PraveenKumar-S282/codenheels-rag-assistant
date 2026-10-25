from app.document_loader import extract_text
from app.chunker import chunk_text
from app.embedder import create_embeddings

pages = extract_text("documents/sample.pdf")

all_chunks = []

for page in pages:
    chunks = chunk_text(page["text"])
    all_chunks.extend(chunks)

embeddings = create_embeddings(all_chunks)

print("Number of chunks:", len(all_chunks))
print("Embedding shape:", embeddings.shape)
print("First embedding:", embeddings[0][:5])