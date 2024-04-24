FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the server app code into the container
COPY chatapp.py /app

# Copy the requirements.txt into the container
COPY requirements.txt /app

# Install dependencies
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the server app
CMD ["python", "chatapp.py", "--host", "0.0.0.0", "--port", "8000", "--redis", "redis"]
