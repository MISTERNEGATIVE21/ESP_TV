import asyncio
import websockets
import cv2
import numpy as np

# Replace with the actual WebSocket server address
server_address = "ws://192.168.4.1:8888"

# Path to the video source
video_source = "./mini.3gp"

# Target dimensions
target_width = 160
target_height = 128

# JPEG quality and color format
jpeg_quality = 10
color_format = cv2.COLOR_RGB2BGR  # Convert to BGR format

# Frame skip interval (skip every N frames)
frame_skip_interval = 15  # Change this value as needed

# Target frame rate (frames per second)
target_fps = 15

# Interval for sending packets (in seconds)
send_interval = 5

async def send_frames():
    cap = cv2.VideoCapture(video_source)
    
    # Calculate frame delay for target FPS
    frame_delay = 1.0 / target_fps

    async with websockets.connect(server_address) as websocket:
        frame_count = 0
        
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame_count += 15

            # Skip frames based on the frame_skip_interval
            if frame_count % frame_skip_interval != 0:
                continue

            # Resize the frame to the target dimensions
            frame = cv2.resize(frame, (target_width, target_height))

            # Convert the frame to RGB565 format
            frame = cv2.cvtColor(frame, color_format)

            # Encode the frame to JPEG format with the specified quality
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])

            # Send the JPEG frame to the WebSocket server
            await websocket.send(buffer.tobytes())

            # Calculate elapsed time and introduce a delay to achieve the target FPS
            await asyncio.sleep(frame_delay)

            # Introduce a sleep interval for sending packets (5 seconds)
            await asyncio.sleep(send_interval)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_frames())
