from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import base64
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Global variable to hold the video capture
video_capture = None

def video_stream():
    global video_capture
    if not video_capture:
        video_capture = cv2.VideoCapture('./mini.3gp')  # Use the test.mp4 file as the video source

    while True:
        success, frame = video_capture.read()
        if not success:
            break

        # Convert the frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = base64.b64encode(buffer).decode('utf-8')

        # Send the frame to all connected clients
        socketio.emit('video_frame', frame_data)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    if not video_capture:
        threading.Thread(target=video_stream).start()

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/video')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8888)
