from app.chains.rag_chain import build_chain
from app.memory.session_history import clear_session_history
from deepeval.tracing import observe, update_current_trace

def serialize_docs(docs):
    return [
        {
            "content": d.page_content,
            "metadata": d.metadata
        }
        for d in docs
    ]

@observe(type="llm",model="Ollama Model",name="Getting Response with Context")
def get_response_with_context(query: str, session_id: str, retriever):
    """Returns (answer, retrieved_chunks) using the same chain as get_response,
    but with a single retrieval call so both are guaranteed to match."""

    retrieved_docs = retriever.invoke(query)
    retrieved_chunks = serialize_docs(retrieved_docs)

    chain_with_message_history=build_chain(retriever)
    answer = chain_with_message_history.invoke(
        {"query": query, "retriever_context": retrieved_chunks},
        config={"configurable": {"session_id": session_id}}
    )

    update_current_trace(
        name = query[:50],  # Use the first 50 chars of the query as the trace name
        input=query,
        output=answer,
        retrieval_context=[chunk['content'] for chunk in retrieved_chunks]
    )
    return answer, retrieved_chunks
