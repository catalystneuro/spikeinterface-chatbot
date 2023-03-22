
# Spikeinterface questions
A flask app based on OpenAI and LangChain to answer questions in the documentation of spikeinterface.

## How to run the app locally?
flask --app spikeinterface_chatbot.app run

## Docker
## How to build the docker image
build -t spikeinterface_chatbot_container .
Where the -t adds the name as a tag of the docker file so it can be referenced later.

## How to run the app from docker
docker run -d -p 5000:80  spikeinterface_chatbot_container

Where the -d is the detach command (so you get back your terminal) and the -p is mapping port 5000 in the local computer to port 80 on the container.

## How to push a docker container to github register container
docker push ghcr.io/{USERNAME}/spikeinterface_chatbot_container:latest

docker tag spikeinterface_chatbot_container ghcr.io/{USERNAME}/spikeinterface_chatbot_container:latest
docker push ghcr.io/{USERNAME}/spikeinterface_chatbot_container:latest
