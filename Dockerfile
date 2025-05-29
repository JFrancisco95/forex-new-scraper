FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    unzip \
    curl \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    libxshmfence-dev \
    libxi6 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Start app
CMD ["python", "main.py"]
