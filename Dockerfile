# Get the base image
FROM python:3.11.3-slim-buster

# # Set the working directory
WORKDIR /app

# Copy requirements files across
COPY requirements.txt requirements.txt

# Install the requirements
RUN pip3 install -r requirements.txt

# Copy the rest of the files across
COPY . .

# Expose the port
EXPOSE 8501

# Set the healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the main file
CMD ["/usr/local/bin/python", "src/main.py"]

