from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableWithMessageHistory

from app.llms.llm_provider import chatmodel
from app.memory.session_history import get_session_history
from app.prompts.prompt_templates import template
from app.retrievers.retriever_factory import build_retriever


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_chain(retriever):

    chain = (
        {
            "retriever_context": RunnableLambda(
                lambda x: x["retriever_context"]
                if "retriever_context" in x
                else format_docs(retriever.invoke(x["query"]))
            ),
            "query": RunnableLambda(lambda x: x["query"]),
            "history": itemgetter("history"),
        }
        | template
        | chatmodel
        | StrOutputParser()
        )

    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="query",
        history_messages_key="history",
    )
