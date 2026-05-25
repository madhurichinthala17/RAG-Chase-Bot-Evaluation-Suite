from langchain_community.document_loaders import PyMuPDFLoader
from app.ingestion.cleaner import clean_text
from pathlib import Path

PDF_PATH = str(Path(__file__).resolve().parent.parent.parent / "data" / "raw_docs" / "JPmorgan10kReport.pdf")

def load_filtered_docs(filepath : str =PDF_PATH):
    loader = PyMuPDFLoader(
    filepath,
    extract_tables="markdown"
    )

    filtered_docs = []

    for doc in loader.lazy_load():

        page_num = doc.metadata.get("page", 0)
        content = doc.page_content.lower()

        # Skip early pages
        if page_num < 3:
            continue

        # Skip noisy pages
        if "glossary of terms and acronyms" in content:
            continue

        if "signatures" in content:
            continue

        cleaned_content = clean_text(doc.page_content)
        doc.page_content = cleaned_content
        filtered_docs.append(doc)

    return filtered_docs
