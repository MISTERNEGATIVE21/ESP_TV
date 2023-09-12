import asyncio
import websockets
import cv2
import numpy as np
import io

# Define the target resolution
target_width = 160
target_height = 128

async def send_jpeg_frames():
    cap = cv2.VideoCapture('./test.mp4')
    if not cap.isOpened():
        print("Error: Could not open video file")
        return

    async with websockets.connect('ws://192.168.4.1:8888') as websocket:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize the frame to the target resolution (160x128)
            frame = cv2.resize(frame, (target_width, target_height))

            # Convert the frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            jpeg_bytes = buffer.tobytes()

            # Send the JPEG frame over WebSocket
            await websocket.send(jpeg_bytes)

            # Wait for 5 seconds before sending the next frame
            await asyncio.sleep(5)

asyncio.get_event_loop().run_until_complete(send_jpeg_frames())
