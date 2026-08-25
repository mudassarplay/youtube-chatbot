from langchain_text_splitters import RecursiveCharacterTextSplitter   # splits long text into smaller chunks
from langchain_huggingface import HuggingFaceEmbeddings                # local embedding model
from langchain_chroma import Chroma                                    # vector store
from langchain_core.documents import Document                          # to wrap text as Document objects

def create_vectorstore(transcript_text: str):
    """Takes raw transcript text, splits it into chunks, embeds them, and returns a Chroma vector store."""

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)   # split into ~1000-char chunks, with overlap so context isn't lost at boundaries
    chunks = splitter.split_text(transcript_text)                                   # returns a list of text chunks

    documents = [Document(page_content=chunk) for chunk in chunks]                  # wrap each chunk as a Document object

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  # your usual local embedding model

    vectorstore = Chroma.from_documents(documents, embedding_model)                 # embed + store all chunks

    return vectorstore