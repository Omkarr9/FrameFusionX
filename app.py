from flask import Flask, render_template, request, send_file, send_from_directory, redirect
from werkzeug.utils import secure_filename
from video_processing import process_video
import os

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}  # Add any other allowed extensions here

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        threshold = request.form['threshold']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            summarized_video, summarized_detection_video, original_video_length, summarized_video_length, unique_frames, similar_frames, total_frames_original, time_saved = process_video(file_path, threshold)

            return render_template('index.html', summarized_video=summarized_video, summarized_detection_video=summarized_detection_video, 
                                   original_video_length=format_time(original_video_length), summarized_video_length=format_time(summarized_video_length),
                                   unique_frames=unique_frames, similar_frames=similar_frames, total_frames=total_frames_original,
                                   time_saved=time_saved)


def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
