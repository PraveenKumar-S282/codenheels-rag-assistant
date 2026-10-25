from functools import lru_cache
from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks: list[str]):
    model = get_model()
    embeddings = model.encode(
        chunks,
        batch_size=8,
        show_progress_bar=False,
    )
    return embeddings
