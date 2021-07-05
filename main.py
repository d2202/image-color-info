from flask import Flask, render_template, url_for, redirect
import image_info

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/image")
def image_info():
    pass


if __name__ == "__main__":
    app.run(debug=True)
