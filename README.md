### **Flask-PyTorch OCR App** 📄🔍  

This repository contains a **Flask-based Optical Character Recognition (OCR) web application** leveraging **Microsoft's TrOCR model (Transformer-based OCR) powered by PyTorch**. The application allows users to extract text from images, process remote images via URLs, and export the extracted content as Word or PDF documents.  

## **Features**  
 **Advanced OCR Processing** using TrOCR (Transformer-based model)  
 **Supports Image Upload & URL-based Text Extraction**  
 **Exports Extracted Text as Word (.docx) & PDF (.pdf)**  
 **Lightweight & Scalable Flask Backend**  

## **Technology Stack**  
- **Flask** – Web framework for API and UI handling  
- **PyTorch & Hugging Face Transformers** – OCR model processing  
- **Pillow & Requests** – Image handling and processing  
- **FPDF & python-docx** – Document generation (PDF & Word)  

## **Installation & Setup**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/flask-pytorch-ocr.git  
   cd flask-pytorch-ocr
   ```  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Run the Flask server:  
   ```bash
   python app.py
   ```  
4. Open the application in your browser:  
   ```
   http://127.0.0.1:5000
   ```  

## **Usage**  
- Upload an image or provide an image URL for text extraction  
- View extracted text on the web interface  
- Download extracted text as a **Word** or **PDF** file  

 

