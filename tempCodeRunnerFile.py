from flask import Flask, render_template, request, send_file, send_from_directory
from werkzeug.utils import secure_filename
from video_processing import process_video
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        threshold = request.form['threshold']  # Get the threshold value from the form
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            summarized_video, summarized_detection_video, unique_frames, similar_frames, total_frames = process_video(file_path, threshold)
            return render_template('index.html', summarized_video=summarized_video, summarized_detection_video=summarized_detection_video, 
                                   unique_frames=unique_frames, similar_frames=similar_frames, total_frames=total_frames)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
