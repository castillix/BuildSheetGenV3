FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for PDF generation fonts)
# RUN apt-get update && apt-get install -y ...

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create directory for generated PDFs if it doesn't exist
RUN mkdir -p generated

EXPOSE 5000

CMD ["python", "app.py"]
