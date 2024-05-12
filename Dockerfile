FROM python:3.8

WORKDIR /core

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Install Gunicorn
COPY gunicorn_config.py .

# Set environment variable (optional, based on your use case)
ENV FLASK_APP=core/server.py

# Specify the entrypoint command
CMD ["gunicorn", "-c", "gunicorn_config.py", "core.server:app"]
