# Use a slim Python 3.11 image
FROM python:3.11-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y build-essential

# Set working directory inside the container
WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install ./technical_exercise-1.0.0-py3-none-any.whl

# Add wait-for-it script
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Start the FastAPI app using uvicorn
CMD ["/wait-for-it.sh", "db:5432", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

