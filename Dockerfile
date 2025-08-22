# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Install ffmpeg, which is a dependency for yt-dlp
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg

# 3. Set the working directory in the container
WORKDIR /app

# 4. Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY . .

# 6. Set the command to run when the container starts
CMD ["python", "-u", "main.py"]
