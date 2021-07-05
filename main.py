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
        secure_path = secure_filename(img.filename)
        print(secure_path)
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_path))
        return redirect(url_for('show_image_info', filename=secure_path))
    return render_template("index.html")


@app.route("/image/<filename>")
def show_image_info(filename):
    file = filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Make lists of colors
    color_names, color_tuples = image_info.make_colors_lists()

    # Convert image into numpy array
    image_colors_array = image_info.open_picture(file_path)

    # Make dict of colors which appear in our img
    colors_dict = image_info.build_colors_dict(color_names, color_tuples, image_colors_array)

    # Make top 10 of colors in image
    top_10_colors = image_info.make_top_10_colors_list(colors_dict)
    # print(top_10_colors)
    # print(len(top_10_colors))
    return render_template("image_info.html", image=file, colors_info=top_10_colors)


if __name__ == "__main__":
    app.run(debug=True)
