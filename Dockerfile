FROM python:3
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY models/ ./models
COPY templates/ ./templates
COPY app.py .

COPY static/ ./static

CMD ["python", "app.py"]