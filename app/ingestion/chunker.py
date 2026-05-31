from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.ingestion.splitter import split_by_sections

def build_chunks(filtered_docs,chunk_size,chunk_overlap) -> list:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    full_text = "\n".join(doc.page_content for doc in filtered_docs)
    sections = split_by_sections(full_text)
    final_docs = []
    for i, section in enumerate(sections):
        for chunk in text_splitter.split_text(section):
            final_docs.append(Document(page_content=chunk, metadata={"section_id": i}))
    return final_docs
