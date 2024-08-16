from langchain.text_splitter import CharacterTextSplitter , RecursiveCharacterTextSplitter
from langchain.document_loaders import  DirectoryLoader , PyPDFLoader , TextLoader
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

file_path = "data"


def create_vector_db_from_text_files():
    # load 1 file.txt
    # loader = TextLoader("data/luat hinh su trang (12).txt")
    # documents = loader.load()
    
    # Load all .txt files from the directory
    loader = DirectoryLoader(
        path="data", 
        glob="*.txt", 
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}  # Specify UTF-8 encoding
    )
    documents = loader.load()

    # Chia nhỏ văn bản
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=512,  # Đặt chunk_size thành 200 ký tự
        chunk_overlap=100,  # Bạn có thể thay đổi giá trị này để điều chỉnh sự trùng lặp
        length_function=len,
    )

    chunks = text_splitter.split_documents(documents)

    for index, item in enumerate(chunks):
        print(f"{index} , {item.page_content}")

    # Load embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Lưu vào database
    db = FAISS.from_documents(chunks, embedding=embedding_model)
    db.save_local("vector_db")

def create_vector_db_from_documents():
    # Load PDF files from directory
    loader = DirectoryLoader(path="data", glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    if not chunks:  
        print("No chunks generated. Skipping embedding creation.")
        return  # Exit the function early
    # Create embeddings
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embedding=embedding_model)

    # Save the database
    db.save_local("vector_db_pdf")


create_vector_db_from_text_files()
# create_vector_db_from_documents()
