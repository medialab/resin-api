FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install Poetry and gunicorn
RUN pip install poetry gunicorn

# Add the current directory to the container as a working directory
ADD . /app

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Expose the port
EXPOSE 8000

ENTRYPOINT bash docker_entrypoint.sh
