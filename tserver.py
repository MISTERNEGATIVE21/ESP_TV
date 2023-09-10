import cv2
from flask import Flask, Response
import time

app = Flask(__name__)

# Replace with the path to your video file
video_source = "./test.mp4"

# Target frame rate (frames per second)
target_fps = 5

# Define the target dimensions
target_width = 160
target_height = 128

# Frame skip interval (skip every N frames)
frame_skip_interval = 5  # Change this value as needed

def generate_frames():
    cap = cv2.VideoCapture(video_source)
    frame_delay = 1.0 / target_fps
    frame_count = 0

    while True:
        start_time = time.time()

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 5

        # Skip frames based on the frame_skip_interval
        if frame_count % frame_skip_interval != 0:
            continue

        # Resize the frame to the target dimensions
        frame = cv2.resize(frame, (target_width, target_height))

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)

        if ret:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        # Calculate elapsed time and introduce a delay to achieve the target FPS
        elapsed_time = time.time() - start_time
        if elapsed_time < frame_delay:
            time.sleep(frame_delay - elapsed_time)

    cap.release()

@app.route('/')
def index():
    return "Welcome to the video streaming server!"

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
