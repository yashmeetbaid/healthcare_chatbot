# Use official Python image as base
FROM python:3.9

# Install required system dependencies for Tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt

# Copy the entire project into the container
COPY . .

# Set display environment variable for GUI applications
ENV DISPLAY=:0

# Command to run the Tkinter application
CMD ["python", "mainWind.py"]
