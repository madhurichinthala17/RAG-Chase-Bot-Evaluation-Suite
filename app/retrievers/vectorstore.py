import os
from pathlib import Path
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from app.ingestion.pdf_loader import load_filtered_docs
from app.ingestion.chunker import build_chunks
from deepeval.tracing import observe,update_current_span

CHROMA_DIR = str(
    Path(__file__).resolve().parent.parent.parent / "data" / "vectorstores" / "chroma_langchain_db"
)

@observe(type="tool", name="creating_vectorstore")
def get_vectorstore(chunk_size:int=800, chunk_overlap:int=600) -> Chroma:
    os.makedirs(CHROMA_DIR, exist_ok=True)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    store = Chroma(
        collection_name="JPMorganSEC",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    if store._collection.count() == 0:
        print(f"[embedding] Vector store empty — building chunks and embedding now...")
        print(f"[embedding] Persisting to: {CHROMA_DIR}")
        filtered_docs = load_filtered_docs()
        chunks = build_chunks(filtered_docs,chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        store.add_documents(chunks)
        print(f"[embedding] Done. {store._collection.count()} chunks stored.")
    else:
        print(f"[embedding] Loaded existing store ({store._collection.count()} chunks) from {CHROMA_DIR}")

    update_current_span(name="Returning Retriever from Vector Store")
    return store
