from flask import Flask, request, redirect, render_template
from database import init_db, insert_url, get_url
from utils import generate_short_code

app = Flask(__name__)
BASE_URL = "http://127.0.0.1:5000/"

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None

    if request.method == "POST":
        original_url = request.form.get("url")

        if not original_url.startswith("http"):
            original_url = "http://" + original_url

        short_code = generate_short_code()
        insert_url(short_code, original_url)

        short_url = BASE_URL + short_code

    return render_template("index.html", short_url=short_url)

@app.route("/<short_code>")
def redirect_url(short_code):
    original_url = get_url(short_code)

    if original_url:
        return redirect(original_url)
    return "URL not found!", 404

if __name__ == "__main__":
    app.run(debug=True)
