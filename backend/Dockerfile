# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in the container
WORKDIR /backend

# Copy the current directory contents into the container at /backend
ADD requirements.txt /backend/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

ADD . /backend/
# Run migrations
#RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8999

# Run the command to start uWSGI
CMD ["uwsgi", "--ini", "/backend/uwsgi.ini"]