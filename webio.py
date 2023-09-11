from flask import Flask, render_template, Response
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import cv2
import time  # Import the time module

app = Flask(__name__)

# Replace './test.mp4' with the path to your video file
video_path = './test.mp4'

cap = cv2.VideoCapture(video_path)

# Define the desired FPS
desired_fps = 15

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        # Get the start time for measuring FPS
        start_time = time.time()
        
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to 160x120
        frame = cv2.resize(frame, (160, 120))

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Calculate the time taken for processing the frame
        elapsed_time = time.time() - start_time

        # Calculate the delay required to achieve the desired FPS
        delay = max(0, 1 / desired_fps - elapsed_time)
        time.sleep(delay)

@app.route('/video_stream')
def video_stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    http_server = WSGIServer(("0.0.0.0", 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
