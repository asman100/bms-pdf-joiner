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
