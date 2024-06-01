FrameFusion is a web application that allows users to upload, process, and summarize videos by removing similar frames and highlighting unique ones. Additionally, it features human detection capabilities to mark detected humans in the summarized videos. This tool is particularly useful for applications in surveillance, sports analysis, and content review, enabling users to quickly navigate through the most relevant parts of a video.

Key Features:
Video Upload: Supports MP4, AVI, and MOV formats.
Threshold Adjustment: Allows users to set a threshold for frame similarity to control the extent of summarization.
Video Processing: Generates two outputs - a summarized video and a summarized video with human detection.
Downloadable Results: Users can download the processed videos directly from the web interface.
Statistics and Feedback: Provides detailed statistics about the video summarization process, including video lengths, unique and similar frame counts, and time saved.


Technologies Used:
Backend: Flask
Frontend: HTML, CSS, Bootstrap
Video Processing: OpenCV, MoviePy
Human Detection: Pre-trained models (MobileNetSSD)
FrameFusion aims to save time and effort in reviewing long videos by focusing on key moments and providing additional context with human detection.

