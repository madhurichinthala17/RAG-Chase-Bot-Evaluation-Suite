from langchain_community.chat_message_histories import ChatMessageHistory
store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def clear_session_history(session_id):
    if session_id in store:
        store.pop(session_id, None)
