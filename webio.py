from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

cap = cv2.VideoCapture('./test.mp4')  # Replace with your video file path

def video_stream():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_data = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_data + b'\r\n')

@socketio.on('connect')
def handle_connect():
    emit('video_stream', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
