FROM kalicyh/uv:v3.13

# Set the working directory in the container
WORKDIR /app

# Copy the server app code into the container
COPY . /app

# Install dependencies
RUN uv sync

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the server app
ENTRYPOINT ["uv", "run", "/app/chatapp.py", "--host", "0.0.0.0", "--port", "8000", "--redis", "redis"]
