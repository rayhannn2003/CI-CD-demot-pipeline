FROM python:3.9-slim

WORKDIR /app

# Copy application source
COPY app/ ./app
COPY app/requirements.txt ./app/requirements.txt
COPY healthcheck.sh ./healthcheck.sh

# Install dependencies
RUN pip install --no-cache-dir -r app/requirements.txt

ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 3000

CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
