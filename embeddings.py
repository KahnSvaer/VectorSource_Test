from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from data_extractor import extract_data


def create_embeddings(url):
    extracted_data = extract_data(url)
    documents = [Document(page_content=content) for content in extracted_data]

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=1)
    chunks = text_splitter.split_documents(documents)
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store


if __name__ == "__main__":
    url = "https://brainlox.com/courses/category/technical"
    vector_store = create_embeddings(url)
    print("Embeddings created and stored in FAISS.")
