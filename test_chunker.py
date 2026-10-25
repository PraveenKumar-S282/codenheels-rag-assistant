from app.document_loader import extract_text
from app.chunker import chunk_text

pages = extract_text("documents/sample.pdf")

for page in pages:
    chunks = chunk_text(page["text"])

    for index, chunk in enumerate(chunks, start=1):
        print(f"Page {page['page']} - Chunk {index}")
        print(chunk)
        print("-" * 30)