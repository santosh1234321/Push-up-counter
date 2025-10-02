# Push-Up Counter
## Features
Upload a video file (mp4, mov, avi) containing push-up exercises.
Automatically detect push-up movements using MediaPipe pose landmarks.
Count completed push-ups based on elbow joint angle.
Display angle and push-up count overlaid on the video.
Download the processed video with visual annotations.

## Requirements
Python 3.7+
streamlit
opencv-python
mediapipe
numpy

## Install dependencies with:
text
pip install streamlit opencv-python mediapipe numpy
Usage
Run the Streamlit app:

text
streamlit run pushup_counter.py
## Steps to use:
Upload your push-up video file via the web interface.
The app processes the video, showing real-time progress.
View the total push-ups counted once processing completes.
Watch the annotated output video and download it if desired.

## How It Works
Uses MediaPipe’s Pose solution to detect body landmarks in each frame.
Calculates the elbow angle to determine push-up position.
Counts one push-up when the elbow moves from bent (< 90°) to extended (> 160°).
Annotates the video with angle, push-up count, and pose landmarks.

## Code Customization
Colors and styles of text and landmarks updated for better visibility.
Output video encoded with H.264 codec for compatibility.

## License
This project is open source under the MIT License.
