import os
from flask import Flask, render_template, url_for, redirect, request
from werkzeug.utils import secure_filename
import image_info

UPLOAD_FOLDER = './static/uploaded_images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if "img" not in request.files:
            return "There is no file in form!"
        img = request.files.get("img")
        # path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
        secure_path = secure_filename(img.filename)
        print(secure_path)
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_path))
        return redirect(url_for('image_info', filename=secure_path))
    return render_template("index.html")


@app.route("/image/<filename>")
def image_info(filename):
    path = filename
    return render_template("image_info.html", image_path=path)


if __name__ == "__main__":
    app.run(debug=True)
