
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def generate_answer(question: str, context: str) -> str:
  
    prompt = f"""
Answer the user's question using the information in the provided document.

Give the answer directly. Do not start with phrases like:
- "Based on the provided context"
- "According to the provided document"
- "Based on the information given"

Write a clear, natural answer.

If the answer cannot be found in the document, say:
"The answer was not found in the uploaded PDF."

Document content:
{context}

Question:
{question}

Answer:
"""


    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    return response.text or "No answer was generated."
