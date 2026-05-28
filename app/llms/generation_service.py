from app.chains.rag_chain import chain_with_message_history
from deepeval.tracing import observe, update_current_trace

@observe(type="llm",model="Ollama Conversational Model")
def get_response(query: str, session_id: str) -> str:
    update_current_trace({"session_id": session_id})
    return chain_with_message_history.invoke(
        {"query": query},
        config={"configurable": {"session_id": session_id}},
    )
    
