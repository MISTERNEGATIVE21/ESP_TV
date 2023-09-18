import cv2
from PIL import Image, ImageDraw, ImageFont

# Define ASCII characters to represent intensity levels
ascii_chars = '@%#*+=-:. '

def frame_to_ascii(frame):
    # Resize the frame to a smaller size
    frame = cv2.resize(frame, (80, 60))

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Initialize an empty ASCII frame
    ascii_frame = Image.new("RGB", (800, 600), "black")
    draw = ImageDraw.Draw(ascii_frame)
    font = ImageFont.load_default()

    # Calculate the width and height of each cell in the ASCII frame
    cell_width = 800 // 80
    cell_height = 600 // 60

    for y in range(60):
        for x in range(80):
            # Get the intensity of the pixel in the grayscale frame
            intensity = gray_frame[y * cell_height, x * cell_width]

            # Map the intensity to an ASCII character
            ascii_char = ascii_chars[intensity // 25]

            # Draw the ASCII character on the frame
            draw.text((x * cell_width, y * cell_height), ascii_char, fill="white", font=font)

    return ascii_frame

# Open the video file
video_capture = cv2.VideoCapture('test.mp4')

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    ascii_frame = frame_to_ascii(frame)

    # Display the ASCII frame
    cv2.imshow('ASCII Video', cv2.cvtColor(np.array(ascii_frame), cv2.COLOR_RGB2BGR))

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
