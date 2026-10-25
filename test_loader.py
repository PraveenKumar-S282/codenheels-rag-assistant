from app.document_loader import extract_text

pages = extract_text("documents/sample.pdf")

for page in pages:
    print(f"Page: {page['page']}")
    print(page["text"])
    print("-" * 40)