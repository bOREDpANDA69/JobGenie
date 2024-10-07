from flask import Flask, request, redirect, url_for, render_template, jsonify
from generateReport import generateReport
import json
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allow only PDF files to be uploaded
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Here you can process the PDF with your existing script
        generateReport(file_path)
        f = open('resume-report\\job_recommendation.json')
        data = json.load(f)
        os.remove(file_path)
        return render_template('results.html', data=data)
    
    return jsonify({'error': 'Invalid file type, only PDFs are allowed'}), 400

if __name__ == "__main__":
    app.run(debug=True)