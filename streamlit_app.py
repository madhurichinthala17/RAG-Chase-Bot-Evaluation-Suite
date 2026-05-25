import streamlit as st
import random
from app.memory.session_history import clear_session_history

st.title("Hey, Welcome to Chase-bot")

session_id= "Madhuri"
session_id = st.text_input("Give a name to our chat so I can remember our conversation!  :)",session_id )

if st.button("Start all new conversation"):
    st.session_state.chat_history =[]
    clear_session_history(session_id)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Lazy import — shows a spinner and surfaces any startup error visibly
# instead of a blank page.
@st.cache_resource(show_spinner="Loading model and vector store...")
def load_chain():
    from app.llms.generation_service import get_response
    return get_response

try:
    get_response = load_chain()
except Exception as e:
    st.error(f"Failed to load the chain: {e}")
    st.stop()

query = st.chat_input("Ask any question about the JP Morgan 10K report")


if query:
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    try:
        answer = get_response(query, "madhuri")
    except Exception as e:
        answer = f"Error: {str(e)}"

    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)