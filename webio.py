from flask import Flask, render_template, Response
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import cv2

app = Flask(__name__)

# Replace './test.mp4' with the path to your video file
video_path = './test.mp4'

cap = cv2.VideoCapture(video_path)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
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

@app.route('/video_stream')
def video_stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    http_server = WSGIServer(("0.0.0.0", 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
