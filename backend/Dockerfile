FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Force installation of pre-compiled wheels only
RUN pip install --only-binary=all -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "app.main"]