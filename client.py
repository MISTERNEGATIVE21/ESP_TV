import asyncio
import websockets
import cv2
import numpy as np

# Define the target resolution
target_width = 160
target_height = 128
color_depth = 256  # 8-bit color depth

async def send_mjpeg_frames():
    cap = cv2.VideoCapture('./test.mp4')
    if not cap.isOpened():
        print("Error: Could not open video file")
        return

    async with websockets.connect('ws://192.168.1.4:8888') as websocket:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize the frame to the target resolution (160x128)
            frame = cv2.resize(frame, (target_width, target_height))

            # Convert the frame to 8-bit color depth
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)

            # Convert the frame to MJPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_bytes = buffer.tobytes()

            # Send the MJPEG frame over WebSocket
            await websocket.send(jpg_bytes)

            # Wait for 5 seconds before sending the next frame
            await asyncio.sleep(6)

asyncio.get_event_loop().run_until_complete(send_mjpeg_frames())
