
import os
import shutil
import tempfile

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.rag_pipeline import answer_question
from app.document_loader import extract_text
from app.chunker import chunk_text
from app.embedder import create_embeddings
from app.vector_store import delete_source, save_chunks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Knowledge Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Stores the currently active PDF filename for local testing.
active_pdf: str | None = None


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI Knowledge Assistant is running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global active_pdf

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            temp_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        pages = extract_text(temp_path)

        if not any(page["text"].strip() for page in pages):
            raise HTTPException(
                status_code=400,
                detail="No readable text found in this PDF."
            )

        chunks = []
        metadatas = []
        ids = []

        for page in pages:
            page_chunks = chunk_text(page["text"])

            for chunk_number, chunk in enumerate(page_chunks):
                chunks.append(chunk)

                metadatas.append({
                    "source": file.filename,
                    "page": page["page"],
                    "chunk": chunk_number,
                })

                ids.append(
                    f"{file.filename}_{page['page']}_{chunk_number}"
                )

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks could be created from this PDF."
            )

        embeddings = create_embeddings(chunks)

        # Remove the old indexed copy of this PDF, if present.
        delete_source(file.filename)

        save_chunks(
            ids=ids,
            chunks=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        # Set this PDF as the active document after indexing succeeds.
        active_pdf = file.filename

        return {
            "message": "PDF uploaded and indexed successfully.",
            "filename": file.filename,
            "pages": len(pages),
            "chunks": len(chunks),
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Failed to process the PDF."
        ) from error

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        await file.close()


@app.post("/ask")
def ask_question(request: QuestionRequest):
    if not active_pdf:
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF first."
        )

    try:
        result = answer_question(
            request.question,
            source=active_pdf,
        )
        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer. Please try again."
        ) from error
