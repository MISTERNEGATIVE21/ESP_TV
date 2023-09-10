import os
import cv2
from flask import Flask, Response, request
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import threading

app = Flask(__name__)

# Initialize video and audio variables as None
video_clip = None
audio_clip = None

def generate_frames():
    global video_clip

    for frame in video_clip.iter_frames(fps=30):  # Adjust the frame rate as needed
        ret, buffer = cv2.imencode('.jpg', frame)

        if ret:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return "Welcome to the video to JPEG and audio player server! Use /video to access the video stream and /audio to play audio."

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/audio', methods=['POST'])
def audio():
    global audio_clip

    audio_start = request.form.get('audio_start', type=int, default=0)
    audio_end = request.form.get('audio_end', type=int, default=None)

    if audio_clip is not None:
        if audio_end is not None:
            audio_clip = audio_clip[audio_start:audio_end]
        else:
            audio_clip = audio_clip[audio_start:]

        threading.Thread(target=play_audio).start()

    return "Audio will play from the specified start time."

def play_audio():
    global audio_clip

    if audio_clip is not None:
        audio_clip.export("temp_audio.wav", format="wav")
        audio = AudioSegment.from_file("temp_audio.wav", format="wav")
        audio.export("temp_audio.mp3", format="mp3")

        audio = AudioSegment.from_mp3("temp_audio.mp3")
        audio.export("temp_audio.wav", format="wav")

        os.system("aplay temp_audio.wav")

if __name__ == "__main__":
    # Replace with the path to your video file
    video_file_path = "./test.mp4"
    audio_file_path = "./test.mp4"
    
    # Load the video and audio clips
    video_clip = VideoFileClip(video_file_path)
    audio_clip = video_clip

    app.run(host='0.0.0.0', port=5000, debug=True)
