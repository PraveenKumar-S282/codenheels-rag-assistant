from pathlib import Path

from app.document_loader import extract_text
from app.chunker import chunk_text
from app.embedder import create_embeddings
from app.vector_store import (
    collection,
    delete_source,
    save_chunks,
)


def index_pdf():
    pdf_path = Path("documents/sample.pdf")

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    pages = extract_text(str(pdf_path))

    chunks = []
    ids = []
    metadatas = []

    for page in pages:
        page_chunks = chunk_text(page["text"])

        for chunk_number, chunk in enumerate(
            page_chunks, start=1
        ):
            chunks.append(chunk)

            ids.append(
                f"{pdf_path.stem}-page-{page['page']}"
                f"-chunk-{chunk_number}"
            )

            metadatas.append({
                "source": pdf_path.name,
                "page": page["page"],
                "chunk": chunk_number,
            })

    if not chunks:
        raise ValueError("No readable text found in PDF")

    embeddings = create_embeddings(chunks)

    # Remove previous chunks from this PDF before re-indexing.
    delete_source(pdf_path.name)

    total = save_chunks(
        ids,
        chunks,
        embeddings,
        metadatas,
    )

    print("PDF indexing completed!")
    print("Chunks processed:", len(chunks))
    print("Total chunks in database:", total)
    print("Sample metadata:", metadatas[0])


if __name__ == "__main__":
    index_pdf()