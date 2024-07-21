from flask import Flask , redirect , url_for , render_template
from dotenv import load_dotenv
import os
# load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("home.html")

@app.route("/contact")
def content():
     return render_template("contact.html")

@app.route("/login")
def login():
     return render_template("login.html")

@app.route("/user/<name>")
def printName(name):
    if name == "admin":
        redirect(url_for("helloAdmin")) # ten cua ham
    return f"<h1>hello {name}</h1>"

@app.route("/blog/<int:blog_id>")
def printBlog(blog_id):
    return f"<h1>blog number {blog_id}</h1>"

@app.route("/admin")
def helloAdmin():
        return "hello admin"




if __name__ =="__main__":
    # Get the port from environment variable or default to 5000
    my_port = int(os.getenv("PORT", 5000)) 
    # os.getenv("PORT") PORT là tên trong file .env còn tham số thứ 2 là để lấy khi ko có port
    print(f"my port {my_port}")
    app.run(debug=True,port=my_port)