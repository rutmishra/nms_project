# Use Python 3.11 as the base image
FROM python:3.11

# Add this line after the base image
RUN apt-get update && apt-get install -y \
    curl \
    python3-psutil

# Set the working directory inside the container
WORKDIR /app

# Copy the backend requirements file and install dependencies
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Add this after installing requirements.txt
RUN pip install psutil==5.9.8

# Copy the entire backend directory to the container
COPY backend/ .

# Copy necessary scripts from the root directory (outside backend)
COPY ../wait-for-it.sh /wait-for-it.sh
COPY ../entrypoint.sh /entrypoint.sh

# Ensure scripts have execution permissions
RUN chmod +x /wait-for-it.sh /entrypoint.sh

# Expose the port Django runs on
EXPOSE 8000

# Use the entrypoint script to start the application
ENTRYPOINT ["/entrypoint.sh"]
