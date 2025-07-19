FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY src/ ./src/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create .env file placeholder
RUN touch .env

# Expose the default MCP port (if needed)
# EXPOSE 3000

# Run the MCP server
CMD ["python", "-m", "src.server"]