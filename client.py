import cv2
import asyncio
import websockets
import io

# Replace './test.mp4' with the path to your video file
#video_path = './mini.3gp'
video_path = './test.mp4'
cap = cv2.VideoCapture(video_path)

# Define the desired FPS
desired_fps = 15

async def send_frames(websocket, path):
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to 160x120
        frame = cv2.resize(frame, (160, 120))

        # Encode the frame as PIX-JPEG
        _, buffer = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

        # Convert the frame to binary
        frame_bytes = buffer.tobytes()

        await websocket.send(frame_bytes)

        # Calculate the delay required to achieve the desired FPS
        await asyncio.sleep(1 / desired_fps)

if __name__ == "__main__":
    start_server = websockets.serve(send_frames, "0.0.0.0", 8888)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
