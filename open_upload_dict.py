import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 设置允许上传的文件类型和目标文件夹
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "jar", "sql", "zip", "md"}
UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
INDEX_HTML = 'index.html'


def allowed_file(filename):
    # 检查文件扩展名是否在允许的范围内
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template(INDEX_HTML)


@app.route('/upload', methods=['POST'])
def upload_file():
    # check file selected
    if 'file' not in request.files:
        return {"message": "No file part"}

    file = request.files['file']

    # check file name
    if file.filename == '':
        return {"message": "No selected file"}

    # check file type
    if not allowed_file(file.filename):
        return {"message": "Invalid file type"}

    # save file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    print("File saved in:", filepath)
    return {"message": "File uploaded"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=50002, debug=False)
