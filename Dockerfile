# Use the Python image for amd64 architecture
FROM --platform=linux/amd64 python:3.12.4-alpine

# Define environment variables
ENV APP_PATH=/opt/web
ENV STATIC_FOLDER_PATH=$APP_PATH/app/static

# Create the application directory and set the working directory
RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH

# Copy the requirements file first to leverage Docker's cache
COPY ./requirements.txt .

# Update packages and add necessary dependencies for Django and PostgreSQL
RUN apk update && \
    apk add --no-cache mariadb-dev postgresql-dev gcc musl-dev libffi-dev bash

# Upgrade pip and install application dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code into the image
COPY . .

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
