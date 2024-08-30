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
