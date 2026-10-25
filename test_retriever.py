
from app.retriever import search_documents

question = input("Ask a question about your PDF: ")

results = search_documents(question, top_k=1)

if not results:
    print("No documents found.")
else:
    for result in results:
        print("\nRetrieved text:")
        print(result["text"])

        print("Source:", result["metadata"]["source"])
        print("Page:", result["metadata"]["page"])
        print("Distance:", round(result["distance"], 4))
        print("-" * 40)
