import os
from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter

_vectorstore = None


def _build_vectorstore():
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "weather_guide.txt")
    with open(data_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    chunks = splitter.split_text(text)
    documents = [Document(page_content=chunk) for chunk in chunks]

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    _vectorstore = FAISS.from_documents(documents, embeddings)
    return _vectorstore


@tool
def search_documents(query: str) -> str:
    """
    Search knowledge base documents for weather safety tips.
    """
    vectorstore = _build_vectorstore()
    docs = vectorstore.similarity_search(query, k=2)
    results = "\n".join([doc.page_content for doc in docs])

    return f"""
Knowledge Base Result:

{results}

Answer only using the above information.
Do not add extra knowledge.
"""
