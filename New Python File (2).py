import asyncio
import websockets
import cv2
import numpy as np

# Define the desired resolution (e.g., FRAMESIZE_VGA)
desired_width = 640
desired_height = 480

# WebSocket server host and port
websocket_server_host = "192.168.4.2"  # Replace with your desired host IP address or "0.0.0.0" for all available interfaces
websocket_server_port = 8888  # Replace with your desired port number

async def handle_client(websocket, path):
    while True:
        try:
            # Capture a frame from your camera or video source
            frame = capture_frame()

            # Resize the frame to the desired resolution
            frame = cv2.resize(frame, (desired_width, desired_height))

            # Encode the frame as JPEG
            _, frame_jpeg = cv2.imencode('.jpg', frame)

            # Convert the frame to bytes
            frame_bytes = frame_jpeg.tobytes()

            # Send the frame to the client over WebSocket
            await websocket.send(frame_bytes)
        except Exception as e:
            print(f"Error sending frame to client: {e}")
            break

def capture_frame():
    # Replace this with your actual code to capture frames from your camera or video source
    # For example, if you're using OpenCV to capture frames from a webcam:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame

if __name__ == "__main__":
    start_server = websockets.serve(handle_client, websocket_server_host, websocket_server_port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
