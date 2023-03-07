from flask import Flask, render_template, request
from pyzbar.pyzbar import decode
from PIL import Image
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    # Get the image from the POST request
    file = request.files['image']

    # Decode the QR code
    img = Image.open(file)
    qr_data = decode(img)[0].data.decode()

    # Save the scanned QR code image to the static folder
    img.save(os.path.join(app.static_folder, 'qr_code.png'))

    print("qr_data:", qr_data)

    return render_template('result.html', qr_data=qr_data)

if __name__ == '__main__':
    app.run(debug=True)
