
from app.embedder import create_embeddings
from app.vector_store import collection


def search_documents(
    question: str,
    top_k: int = 3,
    source: str | None = None,
):
    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty")

    if collection.count() == 0:
        return []

    question_embedding = create_embeddings([question])

    # Search only the requested PDF when source is provided.
    where_filter = {"source": source} if source else None

    query_args = {
        "query_embeddings": question_embedding.tolist(),
        "n_results": min(top_k, collection.count()),
        "include": ["documents", "metadatas", "distances"],
    }

    if where_filter:
        query_args["where"] = where_filter

    results = collection.query(**query_args)

    matches = []

    for i, document in enumerate(results["documents"][0]):
        matches.append({
            "text": document,
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return matches
