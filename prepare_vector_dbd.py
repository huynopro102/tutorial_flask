from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS    


pdf_data_path="data"
vector_db_path="vectorstore/db_faiss"

# tạo ra 1 vector db
# b1 khai báo đoạn txt
# b2 chia nhỏ đoạn txt ra
# b3 chia đoạn txt này ra với các chunk khác nhau
# b4 chia nhỏ xong thì embeding
CharacterTextSplitter_demo="""
Các Tham Số của CharacterTextSplitter
1 / chunk_size: Số lượng ký tự tối đa cho mỗi đoạn (chunk). Đây là tham số bắt buộc.
3 /chunk_overlap: Số lượng ký tự chồng lấp giữa các đoạn (chunk). Điều này giúp bảo đảm ngữ cảnh không bị mất khi chia nhỏ văn bản.
3 /separator: Chuỗi ký tự được sử dụng để tách văn bản thành các đoạn. Mặc định là khoảng trắng (" ").
4 /keep_separator: Một boolean xác định xem có giữ lại ký tự phân cách ở cuối mỗi đoạn văn bản hay không. Mặc định là False.
"""
def create_db_from_text():
    
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

    text_spliter = CharacterTextSplitter(
  separator="\n",
  chunk_size=20, 
  chunk_overlap=5
    )
    chunks = text_spliter.split_text(raw_text)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:")
        print(chunk)
        print()


# embeding
# biến 1 đoạn văn bản thành 1 vertor db đặc trưng , để tìm kiếm hoặc ....
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")  # Sử dụng SentenceTransformerEmbeddings
    # đưa vào Faiss db
    db = FAISS.from_texts(texts=chunks,embedding=embedding_model)
    db.save_local(vector_db_path)
    return db

create_db_from_text()


def create_db_from_text():
    # khai báo 1 loader để quét toàn bộ thư mục data
    