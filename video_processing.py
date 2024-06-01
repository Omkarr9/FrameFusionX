import cv2
import numpy as np
import os
import shutil
from moviepy.editor import VideoFileClip

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

def process_video(input_video_path, threshold_summarization):
    # Human detection parameters
    prototxt = 'MobileNetSSD_deploy.prototxt'
    model = 'MobileNetSSD_deploy.caffemodel'
    threshold_detection = 0.5

    # Get original video duration
    original_video = VideoFileClip(input_video_path)
    original_video_duration = original_video.duration
    original_video.close()
    original_video_length = format_time(original_video_duration)
    
    # Calculate original and summarized video lengths in seconds
    
    # Video summarization parameters
    threshold_summarization = float(threshold_summarization)
    output_summarized_video = 'summarized_video.mp4'
    output_summarized_detection_video = 'summarized_detection_video.mp4'

    # Open the input video file
    video = cv2.VideoCapture(input_video_path)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))  # Frames per second
    total_frames_original = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames in original video

    # Create VideoWriter objects for summarized and detected videos with MP4 codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer_summarized = cv2.VideoWriter(output_summarized_video, fourcc, fps, (width, height))
    writer_detected = cv2.VideoWriter(output_summarized_detection_video, fourcc, fps, (width, height))

    # Initialize variables for summarization and detection
    prev_frame = None
    unique_frames = 0
    similar_frames = 0
    frame_diff_threshold = 10000  # Adjust as needed

    # Load the pre-trained machine learning model for human detection
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    # Main loop to process each frame of the input video
    while True:
        ret, frame = video.read()

        if not ret:
            break

        if prev_frame is None:
            prev_frame = frame
            continue

        # Calculate frame difference for summarization
        frame_diff = np.sum(np.absolute(frame - prev_frame)) / np.size(frame)
        if frame_diff > threshold_summarization:
            writer_summarized.write(frame)
            prev_frame = frame
            unique_frames += 1
        else:
            similar_frames += 1

            # Human detection on summarized frames
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
            net.setInput(blob)
            detections = net.forward()

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > threshold_detection:
                    class_id = int(detections[0, 0, i, 1])
                    if class_id == 15:
                        box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                        (startX, startY, endX, endY) = box.astype("int")
                        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

            writer_detected.write(frame)

    # Release resources
    video.release()
    writer_summarized.release()
    writer_detected.release()
    cv2.destroyAllWindows()

    # Calculate summarized video duration
    summarized_video = VideoFileClip(output_summarized_video)
    summarized_video_duration = summarized_video.duration
    summarized_video.close()
    summarized_video_length = format_time(summarized_video_duration)
    
    original_video_length_seconds = original_video_duration
    summarized_video_length_seconds = summarized_video_duration

    # Move the summarized videos to the UPLOAD_FOLDER directory
    summarized_video_path = os.path.join('uploads', output_summarized_video)
    summarized_detection_video_path = os.path.join('uploads', output_summarized_detection_video)
    
    shutil.move(output_summarized_video, summarized_video_path)
    shutil.move(output_summarized_detection_video, summarized_detection_video_path)

    # Check if summarized video was generated successfully
    if os.path.exists(summarized_video_path):
        return summarized_video_path, summarized_detection_video_path, original_video_length_seconds, summarized_video_length_seconds, unique_frames, similar_frames, total_frames_original, original_video_length_seconds - summarized_video_length_seconds
    else:
        return None, summarized_detection_video_path, original_video_length_seconds, summarized_video_length_seconds, unique_frames, similar_frames, total_frames_original, original_video_length_seconds - summarized_video_length_seconds
