# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Necessary to install sentencepiece
RUN apt-get update && apt-get install -y pkg-config cmake
ENV PKG_CONFIG_PATH=/usr/local/lib/pkgconfig

# Trick to install dependencies and caching them until changing requirements.txt
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install the package so it runs from the container
COPY . /app/
RUN pip install -e .

# This is documentation and good practice but not necessary
EXPOSE 80

# Run app.py when the container launches
CMD ["flask", "--app", "spikeinterface_chatbot.app", "run", "--host", "0.0.0.0", "--port", "80"]
