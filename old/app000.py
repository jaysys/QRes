from io import BytesIO
import codecs
from PIL import Image
from flask import Flask, render_template, request
import qrcode
from pyzbar.pyzbar import decode
import base64


app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/gen', methods=['GET', 'POST'])
def qr_gen():
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(input_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_data = codecs.decode(base64.b64encode(img_buffer.getvalue()), 'ascii')
        return render_template('gen.html', input_text=input_text, img_data=img_data)
    else:
        return render_template('gen.html')


@app.route('/read', methods=['GET', 'POST'])
def qr_read():
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
