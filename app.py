import os
from flask import Flask, request, render_template, send_file, jsonify
from pypdf import PdfWriter, PdfReader
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB limit
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Define the standard order and default insertion pages
PDF_TYPES = [
    {"id": "boq", "name": "BOQ", "default_page": 3},
    {"id": "served_equipment", "name": "Served Equipment", "default_page": 4},
    {"id": "io_points", "name": "I/O Points", "default_page": 5},
    {"id": "riser_diagram", "name": "Riser Diagram", "default_page": 6},
    {"id": "schematic_diagram", "name": "Schematic Diagram", "default_page": 7},
    {"id": "compliance_sheet", "name": "Compliance Sheet", "default_page": 8},
    {"id": "datasheets", "name": "Datasheets", "default_page": 9},
    {"id": "catalog", "name": "Catalog", "default_page": 10}, # Placeholder, will be after datasheets
]

@app.route('/')
def index():
    return render_template('index.html', pdf_types=PDF_TYPES)

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return """
    <html>
    <head>
        <title>File Too Large</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
                color: #f8fafc;
            }
            .error-container {
                text-align: center;
                padding: 2rem;
                background: #1e2442;
                border-radius: 16px;
                max-width: 600px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }
            h1 {
                color: #ef4444;
                font-size: 2rem;
                margin-bottom: 1rem;
            }
            p {
                color: #cbd5e1;
                line-height: 1.6;
                margin-bottom: 1rem;
            }
            .back-button {
                display: inline-block;
                margin-top: 1.5rem;
                padding: 0.75rem 2rem;
                background: linear-gradient(135deg, #6366f1, #8b5cf6);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: transform 0.2s;
            }
            .back-button:hover {
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1>⚠️ Files Too Large</h1>
            <p>The files you're trying to upload exceed the maximum allowed size of 500 MB.</p>
            <p>Please try:</p>
            <ul style="text-align: left; margin: 1rem auto; max-width: 400px;">
                <li>Reducing the file sizes by compressing PDFs</li>
                <li>Uploading fewer files at once</li>
                <li>Splitting large PDFs into smaller ones</li>
            </ul>
            <a href="/" class="back-button">← Go Back</a>
        </div>
    </body>
    </html>
    """, 413

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    if 'template_pdf' not in request.files:
        return "No template PDF provided", 400
    
    template_file = request.files['template_pdf']
    if template_file.filename == '':
        return "No selected template PDF", 400

    merger = PdfWriter()
    template_reader = PdfReader(template_file.stream)
    
    # Add all pages from the template to start
    for page in template_reader.pages:
        merger.add_page(page)

    insertions = []
    
    # Collect files and their insertion points
    for pdf_type in PDF_TYPES:
        pdf_id = pdf_type['id']
        if f'include_{pdf_id}' in request.form:
            if pdf_id in request.files:
                file = request.files[pdf_id]
                if file.filename != '':
                    page_number_str = request.form.get(f'page_{pdf_id}', str(pdf_type['default_page']))
                    try:
                        # Insertion is 'after' a page, so for merging it's the page index + 1
                        page_number = int(page_number_str)
                        insertions.append({'id': pdf_id, 'file': file, 'page': page_number})
                    except ValueError:
                        return f"Invalid page number for {pdf_type['name']}", 400

    # Sort insertions by page number to handle them in order
    insertions.sort(key=lambda x: x['page'])

    # The logic for inserting PDFs is complex because each insertion shifts the page numbers for subsequent insertions.
    # A simpler and more robust approach is to build the new PDF in sections.
    
    final_merger = PdfWriter()
    current_template_page = 0
    
    # Get all pages from the original template
    template_pages = list(template_reader.pages)

    # Handle special case for catalog to be after datasheets
    datasheet_page = None
    for item in insertions:
        if item['id'] == 'datasheets':
            datasheet_page = item['page']
            break
    
    for item in insertions:
        if item['id'] == 'catalog' and datasheet_page is not None:
            # The page number for catalog is now after the datasheet insertion page.
            # We'll make it simple and just place it right after datasheets.
            item['page'] = datasheet_page + 0.1 # Use a float to ensure it's sorted right after

    # Re-sort with potentially updated catalog page
    insertions.sort(key=lambda x: x['page'])

    for insertion in insertions:
        insert_at_page = int(insertion['page'])
        
        # Add template pages up to the insertion point
        while current_template_page < insert_at_page and current_template_page < len(template_pages):
            final_merger.add_page(template_pages[current_template_page])
            current_template_page += 1
            
        # Add the pages from the uploaded PDF
        attachment_reader = PdfReader(insertion['file'].stream)
        for page in attachment_reader.pages:
            final_merger.add_page(page)

    # Add any remaining pages from the template
    while current_template_page < len(template_pages):
        final_merger.add_page(template_pages[current_template_page])
        current_template_page += 1

    # Save the merged PDF to a memory buffer
    output_buffer = io.BytesIO()
    final_merger.write(output_buffer)
    output_buffer.seek(0)
    
    return send_file(
        output_buffer,
        as_attachment=True,
        download_name='merged_document.pdf',
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
