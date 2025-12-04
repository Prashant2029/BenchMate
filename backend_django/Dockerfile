# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run migrations and collect static files
RUN python manage.py migrate --noinput || true
RUN python manage.py collectstatic --noinput || true

# Expose port 8001
EXPOSE 8001

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
