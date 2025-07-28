FROM python:3.9-slim

# Avoid writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run_pipeline.py"]




# FROM python:3.9-slim

# # Avoid creating .pyc files
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set working directory
# WORKDIR /app

# # Copy your requirements file
# COPY requirements.txt .

# # Install dependencies
# RUN pip install --upgrade pip && pip install -r requirements.txt

# # Copy your project code
# COPY . .

# # Run the app (update this based on your entry point)
# CMD ["python", "run_pipeline.py"]
