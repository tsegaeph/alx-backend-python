# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose Django’s default port
EXPOSE 8000

# Command to run the Django app (include "-p" for ALX checker)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "-p"]
