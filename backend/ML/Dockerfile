FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8002
CMD ["uvicorn", "app.ml_main:app", "--host", "0.0.0.0", "--port", "8002"]