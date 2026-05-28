from app.chains.rag_chain import chain_with_message_history
from app.retrievers.retriever_factory import build_retriever
from app.memory.session_history import clear_session_history
from deepeval.tracing import observe, update_llm_span

retriever = build_retriever()
@observe(type="tool",name ="Serialized Retrieved docs")
def serialize_docs(docs):
    return [
        {
            "content": d.page_content,
            "metadata": d.metadata
        }
        for d in docs
    ]

@observe(type="llm",model="Ollama Model")
def get_response_with_context(query: str, session_id: str):
    """Returns (answer, retrieved_chunks) using the same chain as get_response,
    but with a single retrieval call so both are guaranteed to match."""

    retrieved_docs = retriever.invoke(query)
    retrieved_chunks = serialize_docs(retrieved_docs)

    answer = chain_with_message_history.invoke(
        {"query": query, "retriever_context": retrieved_chunks},
        config={"configurable": {"session_id": session_id}}
    )
    return answer, retrieved_chunks
