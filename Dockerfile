FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN playwright install && playwright install-deps

EXPOSE 5000

CMD ["python", "src/web_app/app.py"]
