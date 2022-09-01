from fileinput import filename
from flask import Flask, render_template, request
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

from werkzeug.utils import secure_filename
import os
import uuid as uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "secret key 123456987"


@app.route("/")
def hello():
    return render_template('index.html')

# 另外開一個視窗顯示圖片 show_img_OpenCV
@app.route('/', methods=['GET', 'POST'])
def show_img_OpenCV():
    image_file = request.files['imagefile']
    image_name = secure_filename(image_file.filename)
    image_name = str(uuid.uuid1()) + "_" + image_name
    # save img
    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
    # img path
    image_path = "static/images/" + image_name
    return render_template('index.html', 
        image_path=image_path)



if __name__ == "__main__":
    app.run(debug=True, port=5000)