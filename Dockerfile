# Stage 1: Base build stage
# FROM python:3.11-slim AS builder
FROM debian:bullseye-20250317-slim AS builder 

RUN apt-get update --fix-missing \
    && apt-get install -y sudo

RUN apt-get install -y \ 
    python3 \
    python3-pip \
    libpq-dev

# Create the app directory
RUN mkdir /app
 
# Set the working directory
WORKDIR /app
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip and install dependencies
RUN pip install --upgrade pip 
 
# Copy the requirements file first (better caching)
COPY requirements.txt /app/
 
# Install Python dependencies
# RUN cat /etc/os-release
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Stage 2: Production stage
# FROM python:3.13-slim
# FROM debian:bullseye-20250317-slim

# RUN useradd -m -r appuser && \
#    # mkdir /app && \
#    chown -R appuser /app
 
# Copy the Python dependencies from the builder stage
# COPY --from=builder /usr/local/lib/python3.9/dist-packages/ /usr/local/lib/python3.9/dist-packages/
# COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
# Set the working directory
WORKDIR /app
 
# Copy application code
# COPY --chown=appuser:appuser . .
COPY ./server ./server
COPY ./static ./static
 
# RUN rm .env
# RUN rm db.sqlite3

RUN python3 ./server/manage.py collectstatic --noinput

# Install Nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configure Nginx
COPY ./nginx/nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Set environment variables to optimize Python
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1 
  
# # Expose the application port
# EXPOSE 8000 
 
# # Start the application using Gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "application.wsgi:application"]

# Setup entrypoint
COPY ./scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to non-root user
# USER appuser

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]