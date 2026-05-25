from app.retrievers.vectorstore import get_vectorstore

def build_retriever(k: int = 4):
    store = get_vectorstore()
    return store.as_retriever(search_kwargs={"k": k})
