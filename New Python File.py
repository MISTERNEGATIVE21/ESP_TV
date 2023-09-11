import asyncio
import websockets
import os
import cv2
import numpy as np

async def video_server(websocket, path):
    # Specify the directory where your MP4 video file is stored
    video_path = './test.mp4'  # Change this to your video file's path

    # Open the video file for reading
    cap = cv2.VideoCapture(video_path)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to MJPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_data = buffer.tobytes()

            # Send the MJPEG frame over WebSocket
            await websocket.send(jpg_data)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cap.release()

start_server = websockets.serve(video_server, "0.0.0.0", 8765)  # Change the IP and port as needed

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
