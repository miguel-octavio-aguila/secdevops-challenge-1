# Use an official Python runtime as a parent image
# Using 'slim' keeps the image size smaller
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file *first*
# This leverages Docker's build cache. If requirements.txt doesn't change,
# this layer won't be re-run, speeding up builds.
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code into the container
# We copy the entire 'app' directory
COPY ./app /code/app

# Expose the port the app will run on
# We'll run Uvicorn on port 8000
EXPOSE 8000

# Define the command to run the application
# This tells Docker to start the Uvicorn server
# - 'app.main:app': Find the 'app' object in the 'app/main.py' module
# - '--host 0.0.0.0': Listen on all network interfaces (required inside a container)
# - '--port 8000': Run on port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]