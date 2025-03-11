import os
import io
from flask import Flask, render_template, request, redirect, send_file, send_from_directory
from PIL import Image
import requests
from docx import Document
from fpdf import FPDF
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = './images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load TrOCR Model & Processor
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed")

# Function to extract text from an uploaded image using TrOCR
def extract_text(image_path):
    img = Image.open(image_path).convert("RGB")
    pixel_values = processor(img, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    extracted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return extracted_text

# Function to extract text from an image URL
def extract_text_from_url(image_url):
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_url_image.jpg')
    img.save(img_path)
    return extract_text(img_path)

# Function to save extracted text as a Word document
def save_text_as_word(text, output_filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(request.url)

    image = request.files['image']

    if image.filename == '':
        return redirect(request.url)

    if image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)
        extracted_text = extract_text(image_path)
        return render_template('index.html', extracted_text=extracted_text, image_path=image.filename)

@app.route('/extract_url', methods=['POST'])
def extract_url():
    image_url = request.form['image_url']
    if not image_url:
        return redirect(request.url)
    extracted_text = extract_text_from_url(image_url)
    return render_template('index.html', extracted_text=extracted_text)

@app.route('/save_as_word', methods=['POST'])
def save_as_word():
    extracted_text = request.form['extracted_text']
    if not extracted_text:
        return redirect(request.url)
    output_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_text.docx')
    save_text_as_word(extracted_text, output_filename)
    return send_file(output_filename, as_attachment=True)

# Function to save extracted text as a PDF
def save_text_as_pdf(extracted_text, output_filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, extracted_text)
    pdf.output(output_filename)

@app.route('/save_as_pdf', methods=['POST'])
def save_as_pdf():
    extracted_text = request.form['extracted_text']
    if not extracted_text:
        return redirect(request.url)
    output_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_text.pdf')
    save_text_as_pdf(extracted_text, output_filename)
    return send_file(output_filename, as_attachment=True)

@app.route('/images/<filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
