FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY . .

RUN pip install -r requirements.txt

RUN playwright install

RUN playwright install-deps

EXPOSE 5000

CMD ["python", "src/web_app/app.py"]
