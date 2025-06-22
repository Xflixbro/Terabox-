FROM python:3.11.6

# Install system dependencies including aria2
RUN apt update -y && apt upgrade -y && \
    apt install -y --no-install-recommends git ffmpeg aria2 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .

# Create download directory
RUN mkdir -p /app/download

# Expose ports for the application and aria2c RPC
EXPOSE 80 8080 6800

# Start aria2c daemon and then the bot
CMD ["sh", "-c", "aria2c --enable-rpc --rpc-listen-all --rpc-allow-origin-all --max-connection-per-server=16 --max-concurrent-downloads=16 --split=16 --daemon && python3 bot.py"]
