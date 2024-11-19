from flask import Flask, request, jsonify, render_template
import os
from invoice_processor import InvoiceProcessor

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load the InvoiceProcessor instance
processor = InvoiceProcessor(model_path='models/best.pt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        invoice_data = processor.process_invoice(file_path)
        return jsonify(invoice_data)

if __name__ == '__main__':
    app.run(debug=True)
