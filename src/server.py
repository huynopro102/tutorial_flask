from flask import Flask , redirect , url_for
app = Flask(__name__)



@app.route("/")
def home():
    return "this is a home"

@app.route("/blog/<int:blog_id>")
def blog(blog_id):
    return f"<h1> blog is number {blog_id}<h1/>"

@app.route("/user/<name>")
def user(name):
    if name == "admin":
        return redirect(url_for("admin")) # ten cua ham
    return f"<h1> user number {name}<h1/>"

@app.route("/admin")
def admin():
    return "admin"

if __name__ == '__main__':
    app.run(debug=True)