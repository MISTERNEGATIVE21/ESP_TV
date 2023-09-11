import cv2
import numpy as np
import websocket

# Define the WebSocket server URL (replace with your server's IP and port)
server_url = "ws://your_server_ip:8756"

# Initialize OpenCV window for displaying the video stream
cv2.namedWindow("Video Stream", cv2.WINDOW_NORMAL)

def on_message(ws, message):
    # Decode the received data as JPEG and display it using OpenCV
    jpg_data = np.frombuffer(message, dtype=np.uint8)
    frame = cv2.imdecode(jpg_data, cv2.IMREAD_COLOR)
    cv2.imshow("Video Stream", frame)
    cv2.waitKey(1)

if __name__ == "__main__":
    # Initialize the WebSocket client
    ws = websocket.WebSocketApp(server_url, on_message=on_message)
    
    try:
        ws.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
