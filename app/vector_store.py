
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="knowledge_base",
    metadata={"hnsw:space": "cosine"},
)


def delete_source(source: str):
    collection.delete(
        where={"source": source}
    )


def save_chunks(ids, chunks, embeddings, metadatas):
    if not chunks:
        raise ValueError("No chunks to store")

    if not (
        len(ids) == len(chunks)
        == len(embeddings) == len(metadatas)
    ):
        raise ValueError("Input lengths do not match")

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
    )

    return collection.count()
