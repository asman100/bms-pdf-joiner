# BMS PDF Joiner

This is a simple web application to merge multiple PDF files into a single template PDF at specified page numbers.

## Features

-   Upload a main template PDF.
-   Upload multiple attachment PDFs (BOQ, Schematics, etc.).
-   Choose which attachments to include in the final document.
-   Customize the page number for each insertion.
-   Download the final merged PDF.

## Setup and Installation

### Prerequisites

-   Python 3.6+
-   pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/asman100/bms-pdf-joiner.git
    cd bms-pdf-joiner
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  **Start the Flask application:**
    ```bash
    flask run
    ```
    Or alternatively:
    ```bash
    python app.py
    ```

2.  **Open your web browser:**
    Navigate to `http://127.0.0.1:5000`.

3.  **Use the Web Interface:**
    -   Upload your template PDF.
    -   For each document type you want to include, check the box.
    -   Upload the corresponding PDF file.
    -   Adjust the page number where you want the document to be inserted. The insertion will happen *after* the page number you specify.
    -   Click the "Merge PDFs" button.
    -   Your browser will download the final `merged_document.pdf`.

## How it Works

-   **Frontend:** A simple HTML page with a form to collect the PDF files and insertion preferences.
-   **Backend:** A Flask server that:
    -   Receives the files and form data.
    -   Uses the `pypdf` library to perform the merging operations.
    -   Builds the new PDF by adding pages from the template and attachments in the correct order.
    -   Sends the merged PDF back to the user for download.

## File Size Limits

The application supports uploading PDF files with the following limits:

-   **Maximum individual file size:** 400 MB (client-side validation)
-   **Maximum total upload size:** 450 MB (client-side validation)
-   **Server maximum:** 500 MB (Flask configuration)

If you encounter a "413 Request Entity Too Large" error, try:
-   Compressing your PDF files
-   Uploading fewer files at once
-   Splitting large PDFs into smaller ones

## Production Deployment

### Using Gunicorn (Recommended for Production)

1.  **Install gunicorn** (already included in requirements.txt):
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run with Gunicorn:**
    ```bash
    gunicorn -c gunicorn.conf.py app:app
    ```

### Using Nginx as Reverse Proxy

For production deployments, it's recommended to use Nginx as a reverse proxy in front of Gunicorn:

1.  **Copy the example Nginx configuration:**
    ```bash
    sudo cp nginx.conf.example /etc/nginx/sites-available/bms-pdf-joiner
    ```

2.  **Edit the configuration** to match your domain and file paths.

3.  **Enable the site:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/bms-pdf-joiner /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl reload nginx
    ```

**Important:** The Nginx configuration includes settings to handle large file uploads:
-   `client_max_body_size 500M` - Allows uploads up to 500MB
-   Increased timeout settings for large file processing
-   Disabled request buffering for better memory efficiency

### Troubleshooting 413 Errors

If you're still getting "413 Request Entity Too Large" errors after deployment:

1.  **Check Nginx configuration:** Ensure `client_max_body_size` is set to at least 500M
2.  **Check Gunicorn timeout:** Make sure timeout is set high enough (default 300s in gunicorn.conf.py)
3.  **Check Flask configuration:** Verify `MAX_CONTENT_LENGTH` in app.py is set correctly
4.  **Check your hosting provider:** Some cloud platforms have their own limits that need to be configured separately

## System Requirements

-   Python 3.6 or higher
-   At least 1GB of RAM (2GB+ recommended for large PDFs)
-   Sufficient disk space for temporary file storage
