from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

# ファイルを保存するディレクトリ
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ホームページ (ファイルアップロードフォーム)
@app.route('/')
def index():
    return render_template('page.html')

# ファイルアップロードの処理
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({'error': 'ファイルがありません'}), 400

    files = request.files.getlist('files[]')
    saved_files = []

    for file in files:
        # ファイルを保存
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        saved_files.append(file.filename)

    return jsonify({'message': 'アップロード成功', 'files': saved_files}), 200

if __name__ == '__main__':
    app.run(debug=True)