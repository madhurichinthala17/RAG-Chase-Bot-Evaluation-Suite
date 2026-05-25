from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

PROMPTS_DIR = Path(__file__).resolve().parent


def _load(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


SYSTEM_PROMPT = _load("system_prompt.txt")
QA_PROMPT = _load("qa_prompt.txt")

template = ChatPromptTemplate([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history", optional=True),
    ("human", QA_PROMPT),
])
