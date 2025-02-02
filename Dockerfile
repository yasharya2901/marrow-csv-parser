# Dockerfile
FROM python:3.10-slim

# Prevent Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1

# Set the working directory.
WORKDIR /app

# Copy requirements and install dependencies.
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Expose the port that the app will run on.
EXPOSE 8000

# Default command to run your ASGI server (Uvicorn in this case).
CMD ["uvicorn", "main:asgi_app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
