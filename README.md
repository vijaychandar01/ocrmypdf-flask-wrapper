# OCRmyPDF Flask Wrapper

This project is a Flask application that wraps around OCRmyPDF, providing an easy-to-use web interface for OCR processing of PDF files.

## Project Structure

```plaintext
ocrmypdf-flask-wrapper/
│
├── app/
│   ├── __init__.py                # Initialize the Flask app and configurations
│   ├── routes.py                  # Define the routes and views
│   ├── processing.py              # Contains the PDF processing logic
│   ├── utils.py                   # Utility functions (e.g., for file handling, progress tracking)
│   ├── templates/
│   │   ├── index.html             # Index page template
│   │   ├── progress.html          # Progress tracking page template
│   │   └── partial_download.html  # Partial download template
│   │
│   └── static/
│       └── css/
│           └── styles.css             # CSS styles for the application
│
├── uploads/                       # Folder for uploaded files
├── processed/                     # Folder for processed files
├── .dockerignore                  # Specifies files to ignore in Docker builds
├── .env.template                  # Environment variables template file
├── config.py                      # Configuration settings
├── Dockerfile                     # Docker configuration file
├── gs-9540-linux-x86_64           # Ghostscript binary
├── README.md                      # Project README file
├── requirements.txt               # List of dependencies
└── run.py                         # Run the Flask app
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR
- Ghostscript (version 9.54.0 or higher)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/vijaychandar01/ocrmypdf-flask-wrapper.git
   cd ocrmypdf-flask-wrapper
   ```

2. **Set Up Environment**

   Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install System Dependencies**

   - **Linux:**
   
     ```bash
     sudo apt-get update
     sudo apt-get install -y tesseract-ocr libtesseract-dev
     ```
    
   - **Linux:**
   
     ```bash
     # Optional: Install additional languages other than English
     sudo apt-get install -y tesseract-ocr-fra tesseract-ocr-hin
     ```
   - **Windows:**
   
     Download and install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) and [Ghostscript](https://www.ghostscript.com/download/gsdnld.html). Ensure that both are added to your system's PATH.

   - **Mac:**
   
     ```bash
     brew install tesseract ghostscript
     brew install tesseract-lang
     ```

5. **Configure the Application**

   Edit the `.env` file and `config.py` as needed.

6. **Run the Application**

   ```bash
   python run.py
   ```

7. **Access the Application**

   Open `http://127.0.0.1:5000` in your web browser.

## Docker Setup

### Dockerfile Overview

This project includes a Dockerfile for containerized deployment. Below are the key steps included in the Dockerfile.

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies including JBIG2 encoder dependencies
RUN apt-get update && apt-get install -y \
    wget \
    tesseract-ocr \
    pngquant \
    libjpeg-dev \
    libpng-dev \
    autotools-dev \
    automake \
    libtool \
    libleptonica-dev \
    git \
    build-essential \
    && apt-get clean

# Install additional languages for Tesseract OCR if required
# RUN apt-get install -y tesseract-ocr-fra tesseract-ocr-hin (Uncomment and change to required languages)

# Clone, build, and install JBIG2 encoder
RUN git clone https://github.com/agl/jbig2enc && \
    cd jbig2enc && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make install

# Copy the local Ghostscript binary into the container
COPY gs-9540-linux-x86_64 /usr/local/bin/gs

# Make the Ghostscript binary executable
RUN chmod +x /usr/local/bin/gs

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for the app
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Expose port 5000 for the Flask app to run on
EXPOSE 5000

# Run the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

### Running with Docker

1. **Build the Docker Image**

   ```bash
   docker build -t ocrmypdf-flask-wrapper .
   ```

2. **Run the Docker Container**

   ```bash
   docker run -d -p 5000:5000 ocrmypdf-flask-wrapper
   ```

3. **Access the Application**

   Open `http://127.0.0.1:5000` in your web browser.

## License

This project is licensed under the MIT License.