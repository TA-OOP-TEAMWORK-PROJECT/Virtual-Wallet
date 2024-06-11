# Stage 1: Install dependencies
FROM python:3.12 AS base

# Set environment variables to prevent Python from writing pyc files and to buffer outputs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app
WORKDIR /app

# Copy requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Copy application files and run the app
FROM base AS final

# Copy the entire project directory to the working directory in the container
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Define the command to run the app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

#With the help of A.Daskalov
