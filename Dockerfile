FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app/src/

EXPOSE 5000

CMD ["python", "src/web_app/app.py"]
