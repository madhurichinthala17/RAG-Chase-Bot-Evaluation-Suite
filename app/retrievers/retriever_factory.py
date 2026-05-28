from app.retrievers.vectorstore import get_vectorstore
from deepeval.tracing import observe

@observe(type="retriever", model="Chroma with Ollama Embeddings")
def build_retriever(k: int = 6):
    store = get_vectorstore()
    return store.as_retriever(
        search_type="mmr",
        search_kwargs={
        "k": k,
        "fetch_k": k * 2,  # fetch more to allow for better reranking
        "lambda_mult": 0.5,  # balance between relevance and diversity
        })
