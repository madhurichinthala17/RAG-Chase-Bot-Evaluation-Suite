from deepeval.tracing import observe, update_current_trace
from app.chains.rag_chain import build_chain
from app.retrievers.retriever_factory import build_retriever

_cached_chain = None

def _get_chain():
    global _cached_chain
    if _cached_chain is None:
        retriever = build_retriever()
        _cached_chain = build_chain(retriever)
    return _cached_chain


@observe(type="llm",model="Ollama Conversational Model")
def get_response(query: str, session_id: str) -> str:
    update_current_trace({"session_id": session_id})
    chain = _get_chain()
    return chain.invoke(
        {"query": query},
        config={"configurable": {"session_id": session_id}},
    )

