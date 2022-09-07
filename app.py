from flask import Flask, render_template, request, Response
import cv2
import numpy as np
import matplotlib.pyplot as plt
from camera import Video

from werkzeug.utils import secure_filename
import os
import uuid as uuid

app = Flask(__name__)

# UPLOAD_FOLDER = 'static/images'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = "secret key 123456987"

# === def ===
#02-1 開啟攝影機
def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
            b'Content-Type:  image/jpeg\r\n\r\n' + frame +
            b'\r\n\r\n')


# 因為首頁有使用form上傳，所以要另外加一個route
@app.route("/")
def index():
    return render_template('index.html')

#01-1  另外開一個視窗顯示圖片 show_img_OpenCV
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
        image_path=image_path,
        image_name=image_name)

#01-2  在Flask應用程式中顯示多個影象
@app.route('/pics_show', methods=['GET', 'POST'])
def pics_show():
    IMG_LIST = os.listdir('static/images')
    print(IMG_LIST)
    IMG_LIST = ['images/' + i for i in IMG_LIST]
    print(IMG_LIST)
    return render_template("pics_show.html", imagelist=IMG_LIST)

#02-1 Open Camera
@app.route('/video99999', methods=['GET', 'POST'])
def video():
    return Response(gen(Video()),
        mimetype='multipart/x-mixed-replace; boundary=frame')



# === errorhandler ===
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)