from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from dotenv import load_dotenv
import os

from langchain_community.llms import CTransformers
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Cau hinh
model_file = "models/vinallama-2.7b-chat_q5_0.gguf"

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
Bạn là một trợ lí AI hữu ích. Hãy trả lời người dùng một cách chính xác.

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

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contact")
def content():
    return render_template("contact.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_email = request.form["email"]
        user_password = request.form["password"]
        if user_email and user_password:
            print(user_email)
            print(user_password)
            session["user"] = user_email
            return redirect(url_for("printName"))  # Không truyền tham số name nữa
    return render_template("login.html")

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
    return render_template("chat.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    question = data.get("question")
    response = llm_chain.invoke({"question": question})
    
    # Đảm bảo response là chuỗi văn bản
    answer = str(response)
    
    return jsonify({"answer": answer})


if __name__ == "__main__":
    # Get the port from environment variable or default to 5000
    my_port = int(os.getenv("PORT", 5000))
    print(f"my port {my_port}")
    app.run(debug=True, port=my_port)
