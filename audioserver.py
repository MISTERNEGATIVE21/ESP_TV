import os
from flask import Flask, request, send_file
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import subprocess

app = Flask(__name__)

# Replace with the path to your video file (MP4)
video_file_path = "./test.mp4"

@app.route('/')
def index():
    return "Welcome to the MP4 audio player server! Use /play to start audio playback."

@app.route('/play', methods=['GET', 'POST'])
def play_audio():
    start_time = request.form.get('audio_start', type=int, default=0)
    end_time = request.form.get('audio_end', type=int, default=None)

    if end_time is None:
        end_time = int(VideoFileClip(video_file_path).duration)

    # Extract audio from the video
    audio_clip = AudioSegment.from_file(video_file_path, format="mp4")
    
    # Trim the audio to the specified time range
    audio_clip = audio_clip[start_time * 1000:end_time * 1000]  # Convert to milliseconds

    # Export audio to a temporary MP3 file
    audio_clip.export("temp_audio.mp3", format="mp3")

    # Play the audio using aplay (adjust the command based on your system)
    subprocess.run(["aplay", "temp_audio.mp3"], check=True)

    return "Audio playback completed."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
