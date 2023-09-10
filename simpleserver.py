import http.server
import socketserver
from PIL import Image

# Define the directory containing your JPEG image (current directory)
image_file = "./luffy.jpg"

# Set the IP address and port for the server
ip = "0.0.0.0"  # Listen on all available network interfaces
port = 8080     # Use a port of your choice (e.g., 8080)

# Define the desired resolution
desired_width = 160
desired_height = 128

# Create a custom request handler that allows serving JPEG files
class JPEGRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-type', 'image/jpeg')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        try:
            with open(image_file, 'rb') as f:
                img = Image.open(f)
                img = img.resize((desired_width, desired_height), Image.ANTIALIAS)
                img_bytes = img.tobytes()

                self.send_response(200)
                self.send_header('Content-Length', str(len(img_bytes)))
                self.end_headers()
                self.wfile.write(img_bytes)
        except Exception as e:
            self.send_error(404, "File not found")

# Create an HTTP server with the custom request handler
with socketserver.TCPServer((ip, port), JPEGRequestHandler) as httpd:
    print(f"Serving images from '{image_file}' at http://{ip}:{port}")
    httpd.serve_forever()
