from flask import Flask, send_file
from PIL import Image

app = Flask(__name__)

# Replace with the path to your original JPG image file
original_image_path = "./luffy.jpg"

# Convert the image to 8-bit color
image = Image.open(original_image_path)
image = image.convert('P', palette=Image.ADAPTIVE, colors=256)

# Resize the image to 160x128 pixels
image = image.resize((160, 128))

# Save the resized 8-bit color image to a temporary file
eight_bit_image_path = "./luffy_8bit.png"
image.save(eight_bit_image_path, 'PNG')

@app.route('/')
def index():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>8-Bit Color Image</title>
    </head>
    <body>
        <h1>Welcome to the 8-bit color image server!</h1>
        <p>Use the following link to view the 8-bit color image:</p>
        <a href="/image">View Image</a>
    </body>
    </html>
    """

@app.route('/luffy.jpg')
def view_image():
    return send_file(eight_bit_image_path, mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
