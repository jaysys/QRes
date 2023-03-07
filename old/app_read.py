from flask import Flask, render_template, request
from pyzbar.pyzbar import decode
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # retrieve the uploaded image file
        img_file = request.files['qr_image']
        if img_file:
            # read the image file and decode the QR code
            img = Image.open(img_file)
            qr_data = decode(img)
            if qr_data:
                # retrieve the decoded data and display it
                qr_text = qr_data[0].data.decode('utf-8')
                return render_template('read.html', qr_text=qr_text)
            else:
                return render_template('read.html', error='No QR code found in image')
        else:
            return render_template('read.html', error='No image file uploaded')
    else:
        return render_template('read.html')

if __name__ == '__main__':
    app.run(debug=True)
