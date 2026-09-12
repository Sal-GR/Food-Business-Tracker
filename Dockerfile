FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD flask db upgrade && gunicorn -w 2 -b 0.0.0.0:8000 --preload app:app