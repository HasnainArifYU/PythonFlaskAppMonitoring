# Use official lightweight Python image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install required Python libraries (Flask + Prometheus client)
RUN pip install flask prometheus_client

# Copy everything from your project folder into the container
COPY . /app

# Expose port 5000 so Docker can access it from outside
EXPOSE 5000

# Start your app when the container runs
CMD ["python", "app.py"]


