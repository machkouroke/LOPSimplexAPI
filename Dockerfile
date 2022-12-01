# Set base image (host OS)
FROM python:3.10

# By default, listen on port 5000
EXPOSE 8080/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .


EXPOSE 8080
# Specify the command to run on container start
RUN python3 ./computer/init.py

CMD ["gunicorn"  , "-b", "0.0.0.0:8888", "wsgi:app"]