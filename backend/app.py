from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        file_info = {
            'name': filename,
            'size': os.path.getsize(filepath),
            'type': filename.rsplit('.', 1)[1].lower(),
            'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(file_info), 200

@app.route('/api/files', methods=['GET'])
def list_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(filepath):
            files.append({
                'name': filename,
                'size': os.path.getsize(filepath),
                'type': filename.rsplit('.', 1)[1].lower(),
                'upload_date': datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
            })
    return jsonify(files), 200

@app.route('/api/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'message': 'File deleted'}), 200
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)