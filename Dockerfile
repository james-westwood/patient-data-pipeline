# Get the base image
FROM python:3.11.3-slim-buster

# # Set the working directory
WORKDIR /patient-data-pipeline

# Copy requirements files across
COPY requirements.txt requirements.txt

# Install the requirements
RUN pip3 install -r requirements.txt

# Copy the rest of the files across
COPY . .

# Run the main file
CMD ["/usr/local/bin/python", "src/main.py"]

