from langchain_text_splitters import  CharacterTextSplitter
from sentence_transformers import SentenceTransformer
#Sử dụng HuggingFaceEmbeddings thay cho GPT4AllEmbeddings nếu gặp vấn đề tương thích.
pdf_data_path = "data"
vector_db_path = "vector_db"  # Đảm bảo khai báo biến này nếu chưa khai báo

# hàm tạo ra 1 vector từ 1 đoạn text
def create_vector_db_from_text():
    raw_text = """
Xu hướng nghiên cứu và sử dụng các loại phân 
bón có bổ sung các chất có hoạt tính kích thích sinh 
học giúp nâng cao hiệu quả sử dụng dinh dưỡng là 
xu hướng tất yếu trên thế giới và phát triển nhanh 
trong những năm gần đây nhằm giúp nâng cao hiệu 
quả sử dụng dinh dưỡng trong đất vừa làm giảm thất 
thoát, lãng phí gây ô nhiễm cho môi trường. 
Ngày càng có nhiều bằng chứng khoa học cho 
thấy hiệu quả của việc sử dụng chất hoạt tính kích 
thích sinh học được ứng dụng vào nông nghiệp trên 
các cây trồng khác nhau. Các kết quả nghiên cứu cho 
thấy tác động của các chất hoạt tính sinh học khác 
nhau trên nhiều loại cây trồng như giúp cây phát 
triển rễ, tăng cường sự hấp thu chất dinh dưỡng và 
tăng khả năng chống chịu stress môi trường (Yakhin 
Oleg et al., 2013; Calvo et al., 2014; Bulgari et al., 
2015; Colla and Rouphael, 2015).
"""
    # chia nhỏ văn bản
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=20,
        chunk_overlap=5,  # Đúng tham số là chunk_overlap
        length_function=len,
    )

    chunks = text_splitter.split_text(raw_text)

    # Embedding
    model = SentenceTransformer('all-MiniLM-L6-v2')
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Đưa vào Faiss Vector DB
    # db = FAISS.from_texts(texts=chunks, embedding=embedding_model)
    # db.save_local(vector_db_path)
    # return db


# def create_db_from_files():
#     # Khai báo loader để quét toàn bộ thư mục data
#     loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls=PyMuPDFLoader)
#     documents = loader.load()

#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
#     chunks = text_splitter.split_documents(documents)

#     # Embedding
#     embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     db = FAISS.from_documents(chunks, embedding_model)
#     db.save_local(vector_db_path)
#     return db


create_vector_db_from_text()
# create_db_from_files()
