# Use an official Python runtime as a parent image
FROM python:3.10.4
ENV DATA_DIR=/data

# Set the working directory to /app
WORKDIR /app

COPY ./Docker/dev/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
ENTRYPOINT ["/app/entrypoint.sh"]