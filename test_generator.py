
from app.generator import generate_answer

question = "What is Python?"

context = """
Python is a high-level programming language.
It is popular for web development, automation,
data analysis, and artificial intelligence.
"""

answer = generate_answer(question, context)

print("\nQuestion:", question)
print("Answer:", answer)
