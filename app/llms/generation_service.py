from app.chains.rag_chain import chain_with_message_history


def get_response(query: str, session_id: str) -> str:
    return chain_with_message_history.invoke(
        {"query": query},
        config={"configurable": {"session_id": session_id}},
    )
