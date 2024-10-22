# Use the official Python 3.14.0 slim image
FROM python:alpine

# Set environment variables for production
ENV PYTHONDONTWRITEBYTECODE=1  
# Prevents Python from writing .pyc files to disk
ENV PYTHONUNBUFFERED=1  
# Ensures that output from Python is immediately flushed

# Set the working directory in the container
WORKDIR /app

# Create a virtual environment
RUN python -m venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Install gunicorn separately since it's not in requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copy the rest of the application code to the container
COPY . /app/

# Expose the port Flask will run on
EXPOSE 5000

# Define the command to run the application using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app", "--workers=4"]