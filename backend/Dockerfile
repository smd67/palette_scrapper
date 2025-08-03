# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /backend/src

# Copy the requirements file and install dependencies
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

# Expose the port your application listens on (if applicable)
EXPOSE 8001

# Define the command to run your application
CMD ["poetry", "run", "uvicorn", "src.scraper:app", "--host", "0.0.0.0", "--reload"]