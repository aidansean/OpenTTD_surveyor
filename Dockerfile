FROM python:3-alpine

# Install system dependencies for Cairo
RUN apk add --no-cache build-base cairo-dev

# Install requirements
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy runtime necessary files
COPY src src
COPY config config

# Run
ENTRYPOINT ["python", "/app/src/run.py"]
