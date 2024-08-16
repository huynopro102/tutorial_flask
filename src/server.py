from flask import Flask, redirect, url_for, render_template, request, session, jsonify , flash
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from langchain_community.llms import CTransformers
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from werkzeug.security import generate_password_hash

from datetime import datetime  # Thêm dòng này để nhập datetime
import pytz

# Cau hinh
model_file = "models/vinallama-7b-chat_q5_0.gguf"

# Load LLM
def load_llm(model_file):
    llm = CTransformers(
        model=model_file,
        model_type="llama",
        max_new_tokens=1024,
        temperature=0.01
    )
    return llm

# Tao prompt template
def creat_prompt(template):
    prompt = PromptTemplate(template=template, input_variables=["question"])
    return prompt

# Tao simple chain
def create_simple_chain(prompt, llm):
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain

template = """system
Bạn là một trợ lý AI hữu ích. Trả lời ngắn gọn và chính xác mà không gợi ý thêm bất cứ điều gì.

user
{question}
assistant"""




prompt = creat_prompt(template)
llm = load_llm(model_file)
llm_chain = create_simple_chain(prompt, llm)

# load environment variables from .env file
load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = "QAKpoM2WhY3GVawOJpvDx34u5fKlThji"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Cấu hình cơ sở dữ liệu SQLite
db = SQLAlchemy(app)

# Model User để lưu thông tin người dùng
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))

    user = db.relationship('User', backref=db.backref('chats', lazy=True))
    
@app.route("/")
def home():
    user_email = session.get('user_email', None)
    return render_template('home.html', user_logged_in=user_email is not None, user_email=user_email)

@app.route("/contact")
def content():
    return render_template("contact.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_email = request.form["email"]
        user_password = request.form["password"]
        user = User.query.filter_by(email=user_email).first()

        if user and check_password_hash(user.password, user_password):
            session["user_email"] = user_email  # Lưu email người dùng vào session
            return redirect(url_for("home"))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    
    return render_template("login.html")            
    #     if user_email and user_password:
    #         print(user_email)
    #         print(user_password)
    #         session["user"] = user_email
    #         return redirect(url_for("printName"))  # Không truyền tham số name nữa
    # return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match. Please try again.', 'danger')
    
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop('user_email', None)
    return redirect(url_for('home'))

@app.route("/user")
def printName():
    if "user" in session:
        name = session["user"]
        return f"<h1>hello {name}</h1>"
    return redirect(url_for("login"))

@app.route("/blog/<int:blog_id>")
def printBlog(blog_id):
    return f"<h1>blog number {blog_id}</h1>"

@app.route("/admin")
def helloAdmin():
    return "hello admin"

@app.route("/chat")
def chat():
    user_email = session.get('user_email', None)
    if user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            chat_history = Chat.query.filter_by(user_id=user.id).order_by(Chat.timestamp.asc()).all()
        else:
            chat_history = []
    else:
        chat_history = []
    return render_template('chat.html', user_logged_in=user_email is not None, user_email=user_email, chat_history=chat_history)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    question = request.get_json()["question"]
    answer = llm_chain.invoke({"question": question})["text"].strip()
    
    # Chỉ lưu tin nhắn của người dùng và câu trả lời từ assistant
    if 'user_email' in session:
        user = User.query.filter_by(email=session['user_email']).first()
        if user:
            db.session.add(Chat(user_id=user.id, message=f"You: {question} || Assistant: {answer}"))
            db.session.commit()
    
    # Chỉ trả về câu trả lời của assistant
    return jsonify({"answer": f" {answer}"})



# not found
@app.errorhandler(404)
def page_not_found(e):
    user_email = session.get('user_email', None)
    return render_template("notfound404.html", user_logged_in=user_email is not None, user_email=user_email), 404


if __name__ == "__main__":
    # app.run(debug=True)

    # Tạo bảng nếu chưa tồn tại
    with app.app_context():
        db.create_all()
    
    # Get the port from environment variable or default to 5000
    my_port = int(os.getenv("PORT", 5000))
    print(f"my port {my_port}")
    app.run(debug=True, port=my_port)