# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Install dependencies for Chromium and Chromedriver
RUN apt-get update && apt-get install -y wget gnupg unzip

# Download and install Chromium
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -P /tmp/ \
    && dpkg -i /tmp/google-chrome-stable_current_amd64.deb || apt-get -fy install \
    && rm /tmp/google-chrome-stable_current_amd64.deb

# Download the latest compatible version of Chromedriver
RUN CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP=iobank.py
ENV FLASK_ENV=development

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
