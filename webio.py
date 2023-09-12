import cv2
import asyncio
import websockets
import time
import io

# Replace with the path to your video file
video_source = "./test.mp4"

# Target frame rate (frames per second)
target_fps = 5

# Define the target dimensions
target_width = 160
target_height = 128

# Frame skip interval (skip every N frames)
frame_skip_interval = 5  # Change this value as needed

# JPEG quality and color format
jpeg_quality = 12
color_format = cv2.COLOR_BGR2RGB  # Convert to RGB format

async def generate_frames(websocket, path):
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

        # Convert the frame to RGB format (if not already)
        frame = cv2.cvtColor(frame, color_format)

        # Encode the frame to JPEG format with the specified quality
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])

        # Send the frame to the WebSocket client
        await websocket.send(buffer.tobytes())

        # Calculate elapsed time and introduce a delay to achieve the target FPS
        elapsed_time = time.time() - start_time
        if elapsed_time < frame_delay:
            await asyncio.sleep(frame_delay - elapsed_time)

    cap.release()

start_server = websockets.serve(generate_frames, "0.0.0.0", 8888)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
