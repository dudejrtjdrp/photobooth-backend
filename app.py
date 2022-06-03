import os
from tokenize import String
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sys
from flask_cors import CORS
from os import listdir
from os.path import isfile, join
import io
from base64 import encodebytes
from PIL import Image
from flask import jsonify
import flask_restful as restful
import time
from datetime import datetime
import ssl


app = Flask(__name__)
api = restful.Api(app)
CORS(app)


# 업로드 HTML 렌더링
@app.route('/upload')
def render_file():
    return render_template('upload.html')


# 파일 업로드 처리
@app.route('/fileUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        _, _, files = next(os.walk("./Static"))
        file_count = len(files)
        print(files)
        print(file_count)
        encoded_imges = []
        for idx in range(file_count):
            # encoded_imges.append('http://127.0.0.1:5000/static/' + files[idx])
            encoded_imges.append('http://204.236.180.208:5000/static/' +
                                 files[idx])
        return jsonify({'result': encoded_imges})
        # return str(file_count)
    if request.method == 'POST':
        f = request.files['file']
        # 저장할 경로 + 파일명
        print(app.root_path, file=sys.stdout)
        # f.save('../FE/src/assets/' + secure_filename(f.filename))
        f.save('./Static/' + secure_filename(f.filename))
        return 'uploads 디렉토리 -> 파일 업로드 성공!'


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode(
        'ascii')  # encode as base64
    return encoded_img


if __name__ == '__main__':
    # 서버 실행
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
