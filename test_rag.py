
from app.rag_pipeline import answer_question


question = input("Ask a question about your PDF: ")

result = answer_question(question)

print("\nQuestion:", result["question"])
print("\nAnswer:", result["answer"])

print("\nSources:")

for source in result["sources"]:
    print(
        f"File: {source['source']} | "
        f"Page: {source['page']} | "
        f"Distance: {source['distance']}"
    )
