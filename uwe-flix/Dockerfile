FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /uwe-flix

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Set the environment variables
ENV DJANGO_SETTINGS_MODULE=uweflix.settings
ENV PYTHONUNBUFFERED=1
ENV PGUSER=postgres
ENV PGPASSWORD=postgres
ENV PGDATABASE=uweflix_db

# Expose port 8000 to the host
EXPOSE 8000

# Start the Django development server
#CMD ["python", manage.py", "runserver", "0.0.0.0:8000"]