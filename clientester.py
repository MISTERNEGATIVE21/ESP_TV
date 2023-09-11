import asyncio
import websockets
import binascii

# Function to serve an image to connected clients as a hexadecimal string
async def serve_image(websocket, path):
    try:
        # Open the image file and read its binary data
        with open("./luffy.jpeg", "rb") as image_file:
            image_data = image_file.read()
        
        # Convert binary image data to a hexadecimal string
        hex_image_data = binascii.hexlify(image_data).decode('utf-8')
        
        # Send the hexadecimal image data to the client
        await websocket.send(hex_image_data)
    except FileNotFoundError:
        print("Image file not found.")

# Create and start the WebSocket server
async def main():
    server = await websockets.serve(serve_image, "0.0.0.0", 8888)  # Listen on all available network interfaces

    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
