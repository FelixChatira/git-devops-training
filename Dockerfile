
# Use an official lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy application and tests
COPY app/ ./app/
COPY tests/ ./tests/

# Run the calculator application
CMD ["python", "app/main.py"]
