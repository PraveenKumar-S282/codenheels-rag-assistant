
from time import perf_counter

from app.retriever import search_documents
from app.generator import generate_answer


def answer_question(question: str, source: str | None = None) -> dict:
    # Step 1: Retrieve chunks from the selected PDF
    start = perf_counter()
    results = search_documents(
        question,
        top_k=3,
        source=source,
    )
    print(f"Retrieval time: {perf_counter() - start:.2f} seconds")

    if not results:
        return {
            "question": question,
            "answer": "No relevant information found in the selected PDF.",
            "sources": [],
        }

    # Step 2: Build context from retrieved chunks
    context = "\n\n".join(
        result["text"] for result in results
    )

    # Step 3: Generate the answer
    start = perf_counter()
    answer = generate_answer(question, context)
    print(f"Gemini time: {perf_counter() - start:.2f} seconds")

    # Step 4: Return source page details
    sources = []

    for result in results:
        metadata = result["metadata"]

        sources.append({
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": round(result["distance"], 4),
        })

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }
