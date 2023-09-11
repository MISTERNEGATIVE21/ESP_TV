import http.server
import socketserver

# Define the directory containing your JPEG image (current directory)
image_directory = "./luffy.jpeg"

# Set the IP address and port for the server
ip = "0.0.0.0"  # Listen on all available network interfaces
port = 8080       # Use a port of your choice (e.g., 8080)

# Create a custom request handler that allows serving JPEG files
class JPEGRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-type', 'image/jpeg')
        http.server.SimpleHTTPRequestHandler.end_headers(self)
# Create an HTTP server with the custom request handler
with socketserver.TCPServer((ip, port), JPEGRequestHandler) as httpd:
    print(f"Serving images from '{image_directory}' at http://{ip}:{port}")
    httpd.serve_forever()