# Dockerfile - Django Production Setup

# ============================================
# Stage 1: Base Image
# ============================================
FROM python:3.13-slim

# ============================================
# Stage 2: Set Environment Variables
# ============================================
# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# ============================================
# Stage 3: Set Working Directory
# ============================================
WORKDIR /app

# ============================================
# Stage 4: Install System Dependencies
# ============================================
# These are needed for PostgreSQL and Pillow
# --fix-missing helps with temporary mirror issues
RUN apt-get update && apt-get install -y --fix-missing \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# Stage 5: Install Python Dependencies
# ============================================
# Railway builds from repo root, so use full path
# For local builds, ensure you're in django-learning/myshop/ directory
COPY django-learning/myshop/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# Stage 6: Copy Project Files
# ============================================
# Railway builds from repo root, so copy from django-learning/myshop/
# For local builds, ensure you're in django-learning/myshop/ directory
COPY django-learning/myshop/ .

# ============================================
# Stage 7: Create Required Directories
# ============================================
# Create logs directory for logging configuration
RUN mkdir -p /app/logs

# ============================================
# Stage 8: Copy and make entrypoint script executable
# ============================================
# Copy entrypoint script (will be copied with project files in Stage 6, but make it executable)
RUN chmod +x /app/entrypoint.sh || true

# ============================================
# Stage 9: Collect Static Files
# ============================================
RUN python manage.py collectstatic --noinput

# ============================================
# Stage 10: Expose Port
# ============================================
# Railway will set PORT dynamically, default to 8000 for local development
EXPOSE ${PORT:-8000}

# ============================================
# Stage 11: Run with Entrypoint Script
# ============================================
# Railway will override this with startCommand from railway.json
# But this works for local Docker runs too
CMD ["/app/entrypoint.sh"]

