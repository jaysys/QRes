from flask import Flask, render_template_string, request
import qrcode
from io import BytesIO
import codecs
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
        <form method="POST">
            <label>Enter text to generate QR code:</label>
            <input name="input_text" type="text">
            <input type="submit" value="Generate QR code">
        </form>
    ''')

@app.route('/', methods=['POST'])
def generate_qr_code():
    input_text = request.form.get('input_text')
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(input_text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    img_data = codecs.decode(base64.b64encode(img_buffer.getvalue()), 'ascii')
    return render_template_string('''
        <h3>QR code for "{{ input_text }}"</h3>
        <img src="data:image/png;base64,{{ img_data }}" alt="QR code">
    ''', input_text=input_text, img_data=img_data)



if __name__ == '__main__':
    app.run(debug=True)
