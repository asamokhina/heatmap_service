# Base image
FROM python:3.9-slim-buster

# Install dependencies
RUN apt-get update \
    && apt-get install -y netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install project dependencies
RUN pip install --no-cache-dir poetry

# Copy project files to the container
COPY . /app

# Change working directory
WORKDIR /app

RUN poetry install 

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]