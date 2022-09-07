from flask import Flask, render_template, flash, request, redirect, url_for, Response
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, date
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

from camera import Video
import numpy as np
import cv2
from werkzeug.utils import secure_filename
import os
import uuid as uuid

app = Flask(__name__)

# UPLOAD_FOLDER = 'static/images'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "secret key 123456987"

# === SQL ===
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///picmatching.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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
    # img path
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    # save img
    image_file.save(image_path)
    return render_template('index.html', 
        image_path=image_path)
#01-2  在Flask應用程式中顯示多個影象
@app.route('/pics_show', methods=['GET', 'POST'])
def pics_show():
    IMG_LIST = os.listdir('static/images')
    IMG_LIST = ['images/' + i for i in IMG_LIST]
    return render_template("pics_show.html", 
        imagelist=IMG_LIST)

#02-1 Open Camera
@app.route('/video99999', methods=['GET', 'POST'])
def video():
    return Response(gen(Video()),
        mimetype='multipart/x-mixed-replace; boundary=frame')

#03-1 TemplateMatching
# @app.route('/TemplateMatching')
# def pre_maching():
#     return render_template('TemplateMatching.html')
@app.route('/TemplateMatching', methods=['GET', 'POST'])
def image_maching():
    form = PicmatchForm()

    # if form.validate_on_submit():
    #     pic_match = Picmatch.query.filter_by(id).first()
    #     db.session.add(pic_match)
    #     db.session.commit()
    # flash('圖片成功上傳...')
    pic_upload = Picmatch.query.order_by(Picmatch.date_added)
    return render_template('TemplateMatching.html', 
        form = form,
        pic_upload = pic_upload)

# === errorhandler ===
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# ==== FlaskForm ====
class PicmatchForm(FlaskForm):
    image_file = FileField("圖片上傳")
    standard_pic = FileField("標準品")
    testsample_pic = FileField("比對樣品")
    submit = SubmitField("確認")

# ==== db model ====
class Picmatch(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(256))
    standard_pic = db.Column(db.String(256))
    testsample_pic = db.Column(db.String(256))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Name %r>' % self.name

if __name__ == "__main__":
    app.run(debug=True, port=5000)
