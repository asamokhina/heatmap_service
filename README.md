# Heatmap service

Application that displays heatmaps. `Heatmap service` is a Python web application built with FastAPI and React. It allows users to view and filter data stored in a PostgreSQL database.

### Requirements

Python 3.9+
Node.js 14+
Docker

### Installation

- Clone the repository
- Navigate to the project directory: `cd heatmap_service`
- Start the Docker containers: `docker-compose up --build`
- Wait for the containers to start (may take a few minutes)

### Usage

Navigate to http://localhost:3000 in your web browser to access the application

### API Documentation

View the API documentation at http://localhost:80/docs

### Testing

To run python unit tests locally:
- Install the dependencies: `poetry install `
- Run tests `poetry run pytest`

To run smoke test:
- Install the dependencies: `poetry install `
- Run tests `poetry run python smoke_test.py`