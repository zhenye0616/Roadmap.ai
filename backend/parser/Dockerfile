# Use a lightweight Python base image
FROM python:3.9-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (if you need any)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && python -m pip install --no-cache-dir \
"setuptools<60.0.0" \wheel 
RUN python -m pip install --no-cache-dir numpy==1.21.6
RUN python -m pip install --no-cache-dir --no-build-isolation spacy==2.3.5
RUN python -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz
RUN python -m pip install --no-cache-dir nltk 
RUN python -m nltk.downloader words
RUN python -m nltk.downloader stopwords
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN python -m pip uninstall -y pyresparser \
 && python -m pip install --no-cache-dir \
 https://github.com/OmkarPathak/pyresparser/archive/refs/heads/master.zip
RUN python -m pip install --no-cache-dir playwright
RUN playwright install chromium
RUN playwright install-deps
# Copy application code
COPY . .

# Expose the port your app listens on
EXPOSE 8001

# Start the app with Uvicorn (adjust module path if needed)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
