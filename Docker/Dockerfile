# Use an official Python runtime as a parent image
FROM python:3.10.4
ENV DATA_DIR=/data

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a directory for the data
RUN mkdir /data
RUN chmod +x /app/entrypoint.sh

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN cd /app && python setup.py install

ENTRYPOINT ["/app/entrypoint.sh"]