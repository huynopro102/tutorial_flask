from flask import Flask, redirect, url_for, render_template, request, session
from dotenv import load_dotenv
import os

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

if __name__ == "__main__":
    # Get the port from environment variable or default to 5000
    my_port = int(os.getenv("PORT", 5000))
    print(f"my port {my_port}")
    app.run(debug=True, port=my_port)
