Push-Up Counter 
A Python web application that counts push-ups performed in a video using pose estimation with MediaPipe.

Features
Upload a video file (mp4, mov, avi) containing push-up exercises.

Automatically detect push-up movements using MediaPipe pose landmarks.

Count completed push-ups based on elbow joint angle.

Display angle and push-up count overlayed on the video.

Download the processed video with visual annotations.

Requirements
Python 3.7+

streamlit

opencv-python

mediapipe

numpy

Install dependencies with:

text
pip install streamlit opencv-python mediapipe numpy
Usage
Run the Streamlit app:

text
streamlit run pushup_counter.py
Upload your push-up video file via the web interface.

The app processes the video, displaying real-time progress and showing the total push-ups detected once done.

Watch the output video with annotations and download it if desired.

How It Works
The app uses MediaPipe's Pose solution to detect key body landmarks in each video frame.

Calculates the elbow angle to determine the push-up position.

Counts a push-up each time the elbow angle moves from a bent (less than 90°) to an extended (more than 160°) position.

Annotates the video with angle information, push-up count, and pose landmarks.

Code Customization
Colors and styles of text and landmarks have been updated for better visibility.

Output video is encoded with H.264 codec.

License
This project is open source under the MIT License.

