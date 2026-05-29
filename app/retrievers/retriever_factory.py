from app.retrievers.vectorstore import get_vectorstore
from deepeval.tracing import observe

@observe(type="retriever", model="Chroma with Ollama Embeddings", embedder="nomic-embed-text",name="Building Retriever")
def build_retriever(retriever_type="similarity",k=6,chunk_size=1000,chunk_overlap=500):
    store = get_vectorstore(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    if retriever_type == "mmr":
        return store.as_retriever(
            search_type="mmr",
            search_kwargs={
            "k": k,
            "fetch_k": k * 2,  # fetch more to allow for better reranking
            "lambda_mult": 0.5,  # balance between relevance and diversity
            })
    return store.as_retriever(search_kwargs={"k": k})
