
import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from functools import lru_cache
from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks: list[str]):
    model = get_model()
    embeddings = model.encode(
        chunks,
        batch_size=1,
        show_progress_bar=False,
        convert_to_numpy=True,
    )
    return embeddings
