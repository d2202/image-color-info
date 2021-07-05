import os
from flask import Flask, render_template, url_for, redirect, request
from werkzeug.utils import secure_filename
import image_info

UPLOAD_FOLDER = './static/uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        img = request.files.get("img")
        if not img:
            return """<h1>There is no file in form!</h1>
                <a href="/">Back home</a>"""
        secure_path = secure_filename(img.filename)
        extension = secure_path[-4:].replace(".", "")
        if extension not in ALLOWED_EXTENSIONS:
            return """<h1>File extension not allowed. Please use one of these: png, jpg, jpeg.</h1>
                            <a href="/">Back home</a>"""
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

    # Sum total pixels in image
    all_pixels = 0
    for value in colors_dict.values():
        all_pixels += value

    # Make top 10 dict of colors in image
    top_10_colors = image_info.make_top_10_colors_list(colors_dict, all_pixels)

    return render_template("image_info.html", image=file, colors_info=top_10_colors)


if __name__ == "__main__":
    app.run(debug=True)
